import socket
import pickle

def almacenar_archivo():
    nombre_archivo = input("Ingrese el nombre del archivo a subir: ")
    try:
        with open(nombre_archivo, "rb") as archivo:
            contenido = archivo.read()
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("localhost", 5000))
        mensaje = {
            'accion': 'almacenar',
            'archivo': nombre_archivo,
            'contenido': contenido
        }
        cliente.sendall(pickle.dumps(mensaje))
        respuesta = cliente.recv(1024)
        print(respuesta.decode())
        cliente.close()
    except FileNotFoundError:
        print("El archivo no fue encontrado. Asegúrate de que el nombre sea correcto.")

def recuperar_archivo():
    nombre_archivo = input("Ingrese el nombre del archivo a recuperar: ")
    nuevo_nombre = input("Ingrese el nuevo nombre para el archivo recuperado (o presione Enter para usar el nombre original): ")
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", 5000))
    mensaje = {
        'accion': 'recuperar',
        'archivo': nombre_archivo
    }
    cliente.sendall(pickle.dumps(mensaje))
    contenido = cliente.recv(8192)
    if not nuevo_nombre:
        nuevo_nombre = f"recuperado_{nombre_archivo}"
    with open(nuevo_nombre, "wb") as archivo:
        archivo.write(contenido)
    print(f"Archivo recuperado como '{nuevo_nombre}'")
    cliente.close()

def listar_archivos():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", 5000))
    mensaje = {'accion': 'listar'}
    cliente.sendall(pickle.dumps(mensaje))
    archivos = pickle.loads(cliente.recv(8192))
    print("Archivos disponibles:")
    for archivo in archivos:
        print(f"- {archivo}")
    cliente.close()

def eliminar_archivo():
    nombre_archivo = input("Ingrese el nombre del archivo a eliminar: ")
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", 5000))
    mensaje = {
        'accion': 'eliminar',
        'archivo': nombre_archivo
    }
    cliente.sendall(pickle.dumps(mensaje))
    respuesta = cliente.recv(1024)
    print(respuesta.decode())
    cliente.close()

def comprobar_estado():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", 5000))
    mensaje = {'accion': 'estado'}
    cliente.sendall(pickle.dumps(mensaje))
    estado = pickle.loads(cliente.recv(8192))
    print("Estado del sistema:")
    for nodo, info in estado.items():
        print(f"{nodo}: {info}")
    cliente.close()

def menu():
    while True:
        print("\nSeleccione una opción:")
        print("1. Subir un archivo")
        print("2. Recuperar un archivo")
        print("3. Listar archivos disponibles")
        print("4. Eliminar un archivo")
        print("5. Comprobar el estado del sistema")
        print("6. Salir")
        opcion = input("Ingrese el número de la opción: ")

        if opcion == "1":
            almacenar_archivo()
        elif opcion == "2":
            recuperar_archivo()
        elif opcion == "3":
            listar_archivos()
        elif opcion == "4":
            eliminar_archivo()
        elif opcion == "5":
            comprobar_estado()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú
menu()
