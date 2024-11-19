import os
import socket
import pickle
import argparse
import sys

# Nodo de Almacenamiento: almacena y recupera fragmentos de archivos
class NodoAlmacenamiento:
    def __init__(self, puerto):
        self.puerto = puerto
        self.almacenamiento = {}

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", self.puerto))
        servidor.listen(5)
        print(f"Nodo de almacenamiento iniciado en el puerto {self.puerto}")

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
            print("\nDeteniendo el nodo de almacenamiento...")
            servidor.close()
            sys.exit()

    def procesar_mensaje(self, mensaje, conexion):
        if mensaje['accion'] == 'almacenar_fragmento':
            self.almacenar_fragmento(mensaje['archivo'], mensaje['fragmento'], mensaje['indice'])
            conexion.sendall(b"Fragmento almacenado")
        elif mensaje['accion'] == 'recuperar_fragmento':
            fragmento = self.recuperar_fragmento(mensaje['archivo'], mensaje['indice'])
            conexion.sendall(fragmento)
        else:
            print("Acción desconocida")

    def almacenar_fragmento(self, nombre_archivo, fragmento, indice):
        if nombre_archivo not in self.almacenamiento:
            self.almacenamiento[nombre_archivo] = {}
        self.almacenamiento[nombre_archivo][indice] = fragmento
        print(f"Fragmento {indice} del archivo '{nombre_archivo}' almacenado correctamente")

    def recuperar_fragmento(self, nombre_archivo, indice):
        fragmento = self.almacenamiento.get(nombre_archivo, {}).get(indice, b"")
        print(f"Recuperando fragmento {indice} del archivo '{nombre_archivo}': {fragmento}")
        return fragmento

# Configuración para iniciar el nodo de almacenamiento
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Iniciar un nodo de almacenamiento")
    parser.add_argument("--puerto", type=int, required=True, help="Puerto del nodo de almacenamiento")
    args = parser.parse_args()

    nodo = NodoAlmacenamiento(puerto=args.puerto)
    nodo.iniciar()
