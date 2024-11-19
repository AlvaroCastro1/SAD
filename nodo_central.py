import os
import socket
import pickle
import json
import signal
import sys

# Cargar configuraciones desde config.json
with open("config.json", "r") as archivo_config:
    config = json.load(archivo_config)

# Nodo Central: gestiona la distribución de fragmentos
class NodoCentral:
    def __init__(self):
        self.nodos = config["nodos_almacenamiento"]
        self.puerto = config["puerto_nodo_central"]
        self.tamaño_fragmento = config["tamaño_fragmento"]
        self.archivos = {}  # Diccionario para almacenar información de los archivos

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", self.puerto))
        servidor.listen(5)
        print(f"Nodo central iniciado en el puerto {self.puerto}")

        try:
            while True:
                conexion, direccion = servidor.accept()
                print(f"Conexión recibida de {direccion}")
                try:
                    datos = conexion.recv(1024)
                    mensaje = pickle.loads(datos)
                    self.procesar_mensaje(mensaje, conexion)
                except (ConnectionResetError, BrokenPipeError):
                    print(f"El cliente {direccion} se ha desconectado inesperadamente")
                finally:
                    conexion.close()
                    print(f"Conexión con {direccion} cerrada")
        except KeyboardInterrupt:
            print("\nDeteniendo el nodo central...")
            servidor.close()
            sys.exit()

    def procesar_mensaje(self, mensaje, conexion):
        if mensaje['accion'] == 'almacenar':
            self.almacenar_archivo(mensaje['archivo'], mensaje['contenido'], conexion)
        elif mensaje['accion'] == 'recuperar':
            self.recuperar_archivo(mensaje['archivo'], conexion)
        elif mensaje['accion'] == 'listar':
            self.listar_archivos(conexion)
        elif mensaje['accion'] == 'eliminar':
            self.eliminar_archivo(mensaje['archivo'], conexion)
        elif mensaje['accion'] == 'estado':
            self.comprobar_estado(conexion)
        else:
            print("Acción desconocida")

    def almacenar_archivo(self, nombre_archivo, contenido, conexion):
        fragmentos = [contenido[i:i + self.tamaño_fragmento] for i in range(0, len(contenido), self.tamaño_fragmento)]
        self.archivos[nombre_archivo] = len(fragmentos)  # Guardar la cantidad de fragmentos del archivo
        for i, fragmento in enumerate(fragmentos):
            nodo = self.nodos[i % len(self.nodos)]
            self.enviar_fragmento(nodo, nombre_archivo, fragmento, i)
        conexion.sendall(b"Archivo almacenado exitosamente")

    def listar_archivos(self, conexion):
        # Enviar la lista de archivos al cliente
        conexion.sendall(pickle.dumps(list(self.archivos.keys())))

    def eliminar_archivo(self, nombre_archivo, conexion):
        if nombre_archivo in self.archivos:
            del self.archivos[nombre_archivo]  # Eliminar la información del archivo
            # Aquí también puedes implementar la lógica para eliminar los fragmentos de los nodos
            conexion.sendall(b"Archivo eliminado exitosamente")
        else:
            conexion.sendall(b"Archivo no encontrado")

    def comprobar_estado(self, conexion):
        estado = {f"Nodo {i+1}": nodo for i, nodo in enumerate(self.nodos)}
        conexion.sendall(pickle.dumps(estado))

    def recuperar_archivo(self, nombre_archivo, conexion):
        contenido = b""
        if nombre_archivo in self.archivos:
            for i in range(self.archivos[nombre_archivo]):
                nodo = self.nodos[i % len(self.nodos)]
                contenido += self.solicitar_fragmento(nodo, nombre_archivo, i)
            conexion.sendall(contenido)
        else:
            conexion.sendall(b"Archivo no encontrado")

    def enviar_fragmento(self, nodo, nombre_archivo, fragmento, indice):
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((nodo["host"], nodo["puerto"]))
        mensaje = {
            'accion': 'almacenar_fragmento',
            'archivo': nombre_archivo,
            'fragmento': fragmento,
            'indice': indice
        }
        cliente.sendall(pickle.dumps(mensaje))
        cliente.close()

    def solicitar_fragmento(self, nodo, nombre_archivo, indice):
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((nodo["host"], nodo["puerto"]))
        mensaje = {
            'accion': 'recuperar_fragmento',
            'archivo': nombre_archivo,
            'indice': indice
        }
        cliente.sendall(pickle.dumps(mensaje))
        fragmento = cliente.recv(1024)
        cliente.close()
        return fragmento

# Iniciar el nodo central
nodo_central = NodoCentral()
nodo_central.iniciar()
