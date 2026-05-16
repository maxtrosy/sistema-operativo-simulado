# Documentación detallada del Simulador de Sistema Operativo Básico

## 1. Introducción

Este documento presenta la explicación detallada del simulador de sistema operativo básico desarrollado en Python. El proyecto tiene como finalidad representar, de manera simplificada, algunos conceptos fundamentales de los sistemas operativos, tales como la gestión de procesos, la planificación de CPU, la administración de memoria y la interacción con el usuario mediante una interfaz de consola.

El simulador parte de un código base llamado `POS_simulatedv0.py`, el cual contenía una estructura inicial con clases para procesos, planificación, memoria e interfaz de usuario. A partir de esa base, se desarrolló una versión más completa que incorpora selector de algoritmos de planificación, validaciones de memoria, estados visibles de los procesos, modo demo y pruebas unitarias.

## 2. Objetivo del proyecto

El objetivo principal del proyecto es comprender y aplicar los conceptos básicos de los sistemas operativos mediante la construcción de una simulación funcional. En este sentido, el programa permite observar cómo se crean procesos, cómo se organizan en una cola de planificación, cómo se ejecutan según diferentes algoritmos y cómo se administra una memoria simulada.

De manera específica, el simulador busca:

- Representar procesos con atributos básicos.
- Mostrar el cambio de estado de los procesos.
- Implementar algoritmos de planificación de CPU.
- Simular la asignación y liberación de memoria.
- Controlar errores comunes en la gestión de procesos y memoria.
- Permitir la interacción del usuario mediante un menú en consola.
- Validar la lógica interna del sistema mediante pruebas unitarias.

## 3. Estructura general del proyecto

El proyecto está organizado de la siguiente manera:

```text
sistema-operativo-simulado/
│
├── main.py
├── test_simulador.py
├── README.md
├── DOCUMENTACION.md
├── .gitignore
└── venv/
```

## 4. Descripción de archivos

### 4.1. Archivo `main.py`

El archivo `main.py` contiene toda la lógica principal del simulador. En este archivo se encuentran las clases, funciones auxiliares, menú de usuario y punto de entrada del programa.

Sus componentes principales son:

- Clase `Color`
- Funciones visuales auxiliares
- Clase `Proceso`
- Clase `Planificador`
- Clase `Memoria`
- Función `cargar_demo`
- Funciones de entrada de datos
- Menú principal
- Función `interfaz_usuario`

### 4.2. Archivo `test_simulador.py`

El archivo `test_simulador.py` contiene las pruebas unitarias del proyecto. Estas pruebas permiten verificar que la lógica principal del simulador funcione correctamente sin depender únicamente de la interacción manual del usuario.

Las pruebas validan:

- Creación de procesos.
- Estados de procesos.
- Ejecución completa.
- Ejecución por quantum.
- Agregado de procesos.
- Prevención de procesos duplicados.
- Selección de algoritmos.
- Funcionamiento de FIFO.
- Funcionamiento de SJF.
- Funcionamiento de Round Robin.
- Asignación de memoria.
- Liberación de memoria.
- Errores de memoria.
- Carga del modo demo.

### 4.3. Archivo `README.md`

El archivo `README.md` contiene una explicación general del proyecto, sus funcionalidades principales, instrucciones básicas de ejecución y una descripción corta de los algoritmos implementados.

### 4.4. Archivo `DOCUMENTACION.md`

Este archivo contiene la explicación detallada del funcionamiento interno del simulador. Su propósito es servir como soporte técnico y académico para comprender cómo está construido el programa.

## 5. Componentes principales del simulador

### 5.1. Clase `Color`

La clase `Color` contiene códigos ANSI utilizados para mostrar textos con colores y estilos en la consola.

Esta clase no afecta la lógica principal del sistema operativo simulado, pero mejora la presentación visual del programa. Permite mostrar mensajes de éxito, error, advertencia, estados de procesos y barras de progreso de forma más clara.

Ejemplo:

```python
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    VERDE = "\033[92m"
    ROJO = "\033[91m"
```

### 5.2. Función `c()`

La función `c()` recibe un texto y uno o varios estilos de color. Su función es devolver el texto decorado con códigos ANSI.

Ejemplo:

```python
def c(texto, *estilos):
    return "".join(estilos) + texto + Color.RESET
```

Esta función permite escribir mensajes visuales sin repetir manualmente los códigos de color en todo el programa.

### 5.3. Función `limpiar()`

La función `limpiar()` borra la pantalla de la consola. Utiliza `cls` si el sistema operativo es Windows y `clear` si es Linux o macOS.

```python
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")
```

Esto permite que el menú se vea más ordenado cada vez que el usuario selecciona una opción.

### 5.4. Función `animar_carga()`

La función `animar_carga()` muestra una pequeña animación de carga en la consola. Se utiliza al iniciar el sistema, registrar procesos y apagar el programa.

Esta función es principalmente visual. No modifica procesos ni memoria.

### 5.5. Función `barra_progreso()`

La función `barra_progreso()` genera una barra visual que representa avance o uso de recursos.

Se utiliza en dos contextos principales:

- Para mostrar el avance de ejecución de un proceso.
- Para mostrar el porcentaje de memoria usada.

Ejemplo de salida:

```text
[████████░░░░░░░░░░░░░░░░] 30%
```

## 6. Estados de proceso

El simulador maneja tres estados principales:

```text
Listo
Ejecución
Terminado
```

### 6.1. Estado `Listo`

Un proceso está en estado `Listo` cuando ha sido creado y se encuentra esperando su turno para ser ejecutado por la CPU.

### 6.2. Estado `Ejecución`

Un proceso pasa a estado `Ejecución` cuando entra al procesador y comienza a utilizar la CPU simulada.

### 6.3. Estado `Terminado`

Un proceso pasa a estado `Terminado` cuando finaliza todo su tiempo de ejecución.

### 6.4. Diccionario `ESTADO_BADGE`

El diccionario `ESTADO_BADGE` permite mostrar cada estado como una etiqueta visual en la consola.

```python
ESTADO_BADGE = {
    "Listo"    : c(" LISTO     ", Color.BG_AZUL,     Color.BLANCO, Color.BOLD),
    "Ejecución": c(" EJECUCIÓN ", Color.BG_AMARILLO, Color.BLANCO, Color.BOLD),
    "Terminado": c(" TERMINADO ", Color.BG_VERDE,    Color.BLANCO, Color.BOLD),
}
```

Este bloque pertenece a la parte visual del programa y permite que los estados se identifiquen fácilmente.

## 7. Clase `Proceso`

La clase `Proceso` representa un proceso dentro del sistema operativo simulado.

### 7.1. Atributos de la clase `Proceso`

Cada proceso tiene los siguientes atributos:

```python
self.id
self.nombre
self.tiempo_ejecucion
self.tiempo_restante
self.estado
self.tiempo_inicio
self.tiempo_fin
```

### 7.2. Atributo `id`

Identifica de manera única a cada proceso. Por ejemplo:

```text
P001
P002
P003
```

### 7.3. Atributo `nombre`

Representa el nombre descriptivo del proceso. Por ejemplo:

```text
Sistema de Archivos
Gestor de Red
Monitor del Sistema
```

### 7.4. Atributo `tiempo_ejecucion`

Indica cuánto tiempo necesita el proceso para ejecutarse completamente.

### 7.5. Atributo `tiempo_restante`

Indica cuánto tiempo le falta al proceso para terminar. Este atributo es especialmente importante en Round Robin, porque los procesos pueden ejecutarse parcialmente y luego volver a la cola.

### 7.6. Atributo `estado`

Guarda el estado actual del proceso. Inicialmente, todos los procesos se crean en estado `Listo`.

### 7.7. Método `ejecutar_completo()`

Este método ejecuta un proceso de principio a fin. Se utiliza principalmente en los algoritmos FIFO y SJF.

Flujo del método:

1. Cambia el estado del proceso a `Ejecución`.
2. Guarda el tiempo de inicio.
3. Muestra la información del proceso.
4. Simula la ejecución con una barra de progreso.
5. Cambia el tiempo restante a 0.
6. Cambia el estado a `Terminado`.
7. Guarda el tiempo de finalización.

### 7.8. Método `ejecutar_por_quantum()`

Este método ejecuta un proceso parcialmente según un quantum de tiempo. Se utiliza en el algoritmo Round Robin.

Flujo del método:

1. Cambia el estado del proceso a `Ejecución`.
2. Calcula cuánto tiempo puede ejecutarse en ese turno.
3. Resta ese tiempo del `tiempo_restante`.
4. Si el proceso termina, cambia su estado a `Terminado`.
5. Si no termina, vuelve a estado `Listo` y regresa a la cola.

## 8. Clase `Planificador`

La clase `Planificador` administra la cola de procesos y define el algoritmo de planificación que se usará para ejecutar los procesos.

### 8.1. Atributos principales

```python
self.procesos
self.procesos_ejecutados
self.algoritmo
self.historial
```

### 8.2. Atributo `procesos`

Es una lista que almacena los procesos pendientes por ejecutar.

### 8.3. Atributo `procesos_ejecutados`

Es una lista que almacena los procesos que ya terminaron su ejecución.

### 8.4. Atributo `algoritmo`

Guarda el algoritmo actualmente seleccionado. Por defecto, el programa inicia con:

```text
FIFO
```

### 8.5. Atributo `historial`

Guarda información sobre el orden de finalización de los procesos. Se utiliza para mostrar el resumen final de ejecución.

## 9. Algoritmos de planificación implementados

El simulador implementa tres algoritmos de planificación:

```text
FIFO
SJF
Round Robin
```

### 9.1. Algoritmo FIFO

FIFO significa `First In, First Out`. Este algoritmo ejecuta los procesos en el mismo orden en que fueron agregados a la cola.

Ejemplo:

```text
P001 -> P002 -> P003
```

Si `P001` fue creado primero, será el primero en ejecutarse.

Ventaja:

- Es simple y fácil de implementar.

Desventaja:

- Si el primer proceso tarda mucho, los demás deben esperar.

### 9.2. Algoritmo SJF

SJF significa `Shortest Job First`. Este algoritmo ejecuta primero los procesos con menor tiempo de ejecución.

Ejemplo:

```text
P001 = 5 segundos
P002 = 2 segundos
P003 = 4 segundos
```

Orden de ejecución:

```text
P002 -> P003 -> P001
```

Ventaja:

- Reduce el tiempo promedio de espera.

Desventaja:

- Los procesos largos pueden quedar esperando más tiempo si entran muchos procesos cortos.

### 9.3. Algoritmo Round Robin

Round Robin ejecuta los procesos por turnos mediante un quantum de tiempo.

Ejemplo con quantum de 2 segundos:

```text
P001 ejecuta 2 segundos
P002 ejecuta 2 segundos
P003 ejecuta 2 segundos
P001 vuelve a la cola si no terminó
```

Ventaja:

- Da oportunidad a todos los procesos de usar la CPU.

Desventaja:

- Requiere manejar tiempos restantes y múltiples turnos.

## 10. Selección de algoritmo

El usuario puede elegir el algoritmo desde el menú principal:

```text
6. Seleccionar algoritmo de planif.
```

Luego puede escoger:

```text
1. FIFO
2. SJF
3. Round Robin
```

Internamente, el programa usa el diccionario:

```python
ALGORITMOS = {
    "1": "FIFO",
    "2": "SJF",
    "3": "ROUND ROBIN",
}
```

La función `seleccionar_algoritmo()` recibe la opción seleccionada y actualiza el algoritmo activo.

## 11. Ejecución de procesos

La ejecución se realiza desde la opción:

```text
7. Ejecutar todos los procesos
```

El método `ejecutar()` del planificador revisa cuál algoritmo está activo y llama al método correspondiente:

```python
if self.algoritmo == "FIFO":
    self._ejecutar_fifo()
elif self.algoritmo == "SJF":
    self._ejecutar_sjf()
elif self.algoritmo == "ROUND ROBIN":
    self._ejecutar_round_robin()
```

## 12. Clase `Memoria`

La clase `Memoria` simula la administración de memoria RAM del sistema.

### 12.1. Atributos principales

```python
self.memoria_total
self.memoria_usada
self.asignaciones
```

### 12.2. Atributo `memoria_total`

Representa la cantidad total de memoria disponible. En el proyecto se configuró como:

```text
1024 MB
```

### 12.3. Atributo `memoria_usada`

Representa la cantidad de memoria actualmente asignada.

### 12.4. Atributo `asignaciones`

Es un diccionario que guarda la memoria asignada a cada proceso.

Ejemplo:

```python
{
    "P001": 128,
    "P002": 64,
    "P003": 256
}
```

### 12.5. Propiedad `memoria_libre`

Calcula la memoria disponible:

```python
return self.memoria_total - self.memoria_usada
```

### 12.6. Propiedad `porcentaje_uso`

Calcula el porcentaje de memoria usada:

```python
return self.memoria_usada / self.memoria_total
```

## 13. Asignación de memoria

La asignación de memoria se realiza desde la opción:

```text
3. Asignar memoria a proceso
```

El método encargado es:

```python
asignar(id_proceso, tamaño, planificador)
```

Antes de asignar memoria, el programa valida:

1. Que el proceso exista.
2. Que el proceso no tenga memoria asignada previamente.
3. Que el tamaño solicitado sea mayor que 0.
4. Que haya suficiente memoria disponible.

Si todas las condiciones se cumplen, se registra la asignación y se actualiza la memoria usada.

## 14. Liberación de memoria

La liberación de memoria se realiza desde la opción:

```text
4. Liberar memoria de proceso
```

El método encargado es:

```python
liberar(id_proceso)
```

Este método verifica si el proceso tiene memoria asignada. Si existe una asignación, elimina el registro y resta ese valor de la memoria usada.

## 15. Modo demo

El modo demo se ejecuta desde la opción:

```text
0. Cargar demo de prueba
```

Este modo crea automáticamente tres procesos:

```text
P001 - Sistema de Archivos - 4 segundos
P002 - Gestor de Red - 2 segundos
P003 - Monitor del Sistema - 6 segundos
```

También asigna memoria automáticamente:

```text
P001 -> 128 MB
P002 -> 64 MB
P003 -> 256 MB
```

El modo demo permite probar el simulador rápidamente sin tener que ingresar datos manualmente.

## 16. Interfaz de usuario

La interfaz principal está implementada en la función:

```python
interfaz_usuario()
```

Esta función contiene un ciclo `while True` que mantiene el programa activo hasta que el usuario seleccione la opción de salir.

El menú principal ofrece las siguientes opciones:

```text
0. Cargar demo de prueba
1. Crear proceso
2. Ver lista de procesos
3. Asignar memoria a proceso
4. Liberar memoria de proceso
5. Ver estado de memoria
6. Seleccionar algoritmo de planif.
7. Ejecutar todos los procesos
8. Salir
```

## 17. Validaciones implementadas

El programa incluye varias validaciones para evitar errores comunes.

### 17.1. Validación de proceso duplicado

No se permite crear dos procesos con el mismo ID.

### 17.2. Validación de proceso inexistente

No se permite asignar memoria a un proceso que no ha sido creado.

### 17.3. Validación de memoria duplicada

No se permite asignar memoria dos veces al mismo proceso.

### 17.4. Validación de memoria insuficiente

No se permite asignar más memoria de la disponible.

### 17.5. Validación de tamaño inválido

No se permite asignar memoria igual o menor que cero.

### 17.6. Validación de algoritmo inválido

Si el usuario selecciona una opción de algoritmo no existente, el sistema muestra un error.

## 18. Pruebas unitarias

El proyecto incluye un archivo de pruebas unitarias llamado:

```text
test_simulador.py
```

Estas pruebas fueron desarrolladas con el módulo `unittest` de Python.

### 18.1. Comando para ejecutar las pruebas

```powershell
python test_simulador.py
```

También se pueden ejecutar con:

```powershell
python -m unittest test_simulador.py
```

### 18.2. Resultado obtenido

Durante la ejecución de las pruebas se obtuvo el siguiente resultado:

```text
Ran 32 tests in 0.025s

OK
```

Esto significa que se ejecutaron 32 pruebas unitarias y todas pasaron correctamente.

### 18.3. Qué validan las pruebas

Las pruebas validan:

- Que los procesos se creen correctamente.
- Que los procesos inicien en estado `Listo`.
- Que la ejecución completa termine el proceso.
- Que Round Robin actualice correctamente el tiempo restante.
- Que el planificador agregue procesos.
- Que no se permitan procesos duplicados.
- Que se puedan buscar procesos.
- Que se puedan seleccionar algoritmos.
- Que FIFO respete el orden de llegada.
- Que SJF ordene por menor tiempo.
- Que Round Robin finalice todos los procesos.
- Que la memoria se asigne correctamente.
- Que no se asigne memoria a procesos inexistentes.
- Que no se asigne memoria duplicada.
- Que no se asigne memoria negativa o cero.
- Que no se asigne memoria excesiva.
- Que la memoria se libere correctamente.
- Que el modo demo cargue tres procesos y sus asignaciones.

## 19. Ejemplo de ejecución recomendada para capturas

Para mostrar el funcionamiento del simulador en el documento de entrega, se recomienda seguir esta secuencia:

```text
1. Ejecutar el programa con python main.py.
2. Seleccionar la opción 0 para cargar el demo.
3. Ver la lista de procesos con la opción 2.
4. Ver el estado de memoria con la opción 5.
5. Seleccionar el algoritmo con la opción 6.
6. Ejecutar los procesos con la opción 7.
7. Tomar captura del resumen final.
8. Ejecutar las pruebas con python test_simulador.py.
9. Tomar captura del resultado OK.
```

## 20. Conclusión

El simulador desarrollado permite comprender de manera práctica cómo un sistema operativo puede organizar procesos, asignarles tiempo de CPU y administrar memoria. Aunque no se trata de un sistema operativo real, el programa reproduce de forma sencilla los comportamientos principales estudiados en clase.

La implementación de tres algoritmos de planificación permite comparar diferentes criterios de ejecución. FIFO muestra el orden de llegada, SJF prioriza los procesos más cortos y Round Robin distribuye la CPU en turnos mediante un quantum.

La gestión de memoria permite observar cómo un sistema controla recursos limitados, evitando asignaciones duplicadas, procesos inexistentes o exceso de memoria. Además, las pruebas unitarias demuestran que la lógica principal del simulador funciona correctamente.

En conclusión, el proyecto cumple con los requisitos planteados y permite aplicar los conceptos fundamentales de procesos, planificación de CPU, memoria e interacción con el usuario.