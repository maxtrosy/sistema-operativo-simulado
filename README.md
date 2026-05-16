# Simulador de Sistema Operativo Básico

## Descripción del proyecto

Este proyecto corresponde a una simulación básica de un sistema operativo desarrollada en Python. El programa permite representar de manera sencilla algunos conceptos fundamentales de los sistemas operativos, como la creación de procesos, la planificación de CPU, la gestión de memoria y la interacción con el usuario mediante una interfaz por consola.

El simulador fue construido a partir del archivo base `POS_simulatedv0.py`, pero se amplió para incluir una interfaz más completa, selector de algoritmos de planificación, control de memoria, validaciones y pruebas unitarias.

## Objetivo

Comprender y aplicar los conceptos básicos de los sistemas operativos mediante la implementación de un simulador funcional que permita:

- Crear procesos.
- Visualizar el estado de los procesos.
- Seleccionar algoritmos de planificación de CPU.
- Ejecutar procesos según el algoritmo seleccionado.
- Asignar y liberar memoria.
- Controlar errores como procesos duplicados, memoria insuficiente o procesos inexistentes.
- Validar el funcionamiento mediante pruebas unitarias.

## Tecnologías utilizadas

- Python 3
- Interfaz por consola
- Módulo `unittest` para pruebas unitarias

## Estructura del proyecto

```text
sistema-operativo-simulado/
│
├── main.py
├── test_simulador.py
├── README.md
├── .gitignore
└── venv/