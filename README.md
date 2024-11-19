# Sistema de Archivos Distribuido

## Descripción
En este proyecto se implementa un sistema básico de archivos distribuido en Python. El cual permite almacenar archivos fragmentados en varios nodos de almacenamiento y recuperarlos de manera eficiente. También incluye funcionalidades para listar archivos, eliminar archivos y comprobar el estado de los nodos.

## Características
- **Almacenar archivos**: Fragmenta un archivo y distribuye los fragmentos a diferentes nodos de almacenamiento.
- **Recuperar archivos**: Reúne los fragmentos desde los nodos y reconstruye el archivo original.
- **Listar archivos disponibles**: Muestra todos los archivos que se han almacenado en el sistema.
- **Eliminar un archivo**: Elimina un archivo almacenado del sistema.
- **Comprobar el estado del sistema**: Muestra el estado de los nodos de almacenamiento.

## Estructura del Proyecto
- **nodo_central.py**: El nodo central que gestiona la fragmentación y distribución de archivos.
- **nodo_almacenamiento.py**: Los nodos de almacenamiento que guardan y devuelven los fragmentos.
- **cliente.py**: El cliente que interactúa con el sistema para realizar acciones.
- **config.json**: Archivo de configuración para definir los nodos y el tamaño de fragmento.
- **README.md**: Documentación del proyecto.

## Requisitos
- Python 3.x
- Para este proyecto no se requieren librerias externas, solo las siguientes librerias de Python:
  - `socket`
  - `pickle`
  - `json`
  - `sys`

## Configuración
1. **Configurar `config.json`**:
   ```json
   {
     "puerto_nodo_central": 5000,
     "nodos_almacenamiento": [
       { "host": "localhost", "puerto": 5001 },
       { "host": "localhost", "puerto": 5002 }
     ],
     "tamaño_fragmento": 1024  // es el tamaño en bytes para la fragmentación
   }
   ```
   - **puerto_nodo_central**: El puerto en el que el nodo central escucha las conexiones.
   - **nodos_almacenamiento**: Lista de nodos de almacenamiento con sus direcciones y puertos.
   - **tamaño_fragmento**: El tamaño en bytes con el que se dividirán los archivos.

## Instrucciones de Uso
### 1. Iniciar los Nodos de Almacenamiento
Para poder ejecutar este proyecto se necesitan varias terminales y ejecutar los siguientes comandos para iniciar cada nodo de almacenamiento:
```bash
python nodo_almacenamiento.py --puerto 5001
python nodo_almacenamiento.py --puerto 5002
```
*(Se pueden iniciar más nodos si es necesario, cambiando el número de puerto).*

### 2. Iniciar el Nodo Central
En **otra** terminal, iniciar el nodo central:
```bash
python nodo_central.py
```

### 3. Ejecutar el Cliente
Ejecutar el cliente en otra **terminal** para **interactuar** con el sistema:
```bash
python cliente.py
```

### 4. Opciones del Cliente
1. **Subir un archivo**: Se debe proporcionar el nombre del archivo que se desea subir. El archivo se fragmentará y distribuirá entre los nodos.
2. **Recuperar un archivo**: Se debe proporcionar el nombre del archivo a recuperar. Se puedes especificar un nombre diferente para el archivo descargado.
3. **Listar archivos disponibles**: Muestra todos los archivos almacenados en el sistema.
4. **Eliminar un archivo**: Elimina un archivo del sistema.
5. **Comprobar el estado del sistema**: Muestra el estado de los nodos de almacenamiento.
6. **Salir**: Cierra el cliente.

## Ejemplo de Uso
1. Para subir un archivo llamado `prueba1.txt`:
   ```
   Ingrese el nombre del archivo a subir: prueba1.txt
   $> Archivo almacenado exitosamente
   ```
2. Para recuperar el archivo:
   ```
   Ingrese el nombre del archivo a recuperar: prueba1.txt
   Ingrese el nuevo nombre para el archivo recuperado (o presione Enter para usar el nombre original): archivo_recuperado.txt
   $> Archivo recuperado como 'archivo_recuperado.txt'
   ```
3. Para listar archivos disponibles:
   ```
   $> Archivos disponibles:
   - prueba1.txt
   ```

## Consideraciones
- **Manejo de Errores**: El sistema maneja desconexiones inesperadas y errores básicos.
- **Extensibilidad**: Se pueden agregar más funcionalidades, como cifrado de archivos o replicación para mayor seguridad.

## Autores
- Álvaro Jesus Castro Pizaña
