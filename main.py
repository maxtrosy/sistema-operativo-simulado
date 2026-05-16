import time
import sys
import os

# ═══════════════════════════════════════════════════════════
#   COLORES Y ESTILOS ANSI
# ═══════════════════════════════════════════════════════════

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Texto
    BLANCO  = "\033[97m"
    GRIS    = "\033[90m"
    ROJO    = "\033[91m"
    VERDE   = "\033[92m"
    AMARILLO= "\033[93m"
    AZUL    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"

    # Fondo
    BG_AZUL     = "\033[44m"
    BG_VERDE    = "\033[42m"
    BG_ROJO     = "\033[41m"
    BG_AMARILLO = "\033[43m"
    BG_NEGRO    = "\033[40m"
    BG_MAGENTA  = "\033[45m"
    BG_CYAN     = "\033[46m"


def c(texto, *estilos):
    return "".join(estilos) + texto + Color.RESET


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def animar_carga(mensaje, duracion=0.8):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    pasos = int(duracion / 0.08)
    for i in range(pasos):
        frame = frames[i % len(frames)]
        print(f"\r  {c(frame, Color.CYAN, Color.BOLD)}  {c(mensaje, Color.GRIS)}", end="", flush=True)
        time.sleep(0.08)
    print(f"\r  {c('✓', Color.VERDE, Color.BOLD)}  {c(mensaje, Color.GRIS)}{' ' * 5}")


def barra_progreso(actual, total, ancho=28, color=Color.AZUL):
    relleno = int((actual / total) * ancho)
    vacio   = ancho - relleno
    barra   = c("█" * relleno, color) + c("░" * vacio, Color.GRIS)
    pct     = int((actual / total) * 100)
    return f"[{barra}] {c(str(pct) + '%', Color.BOLD)}"


# ═══════════════════════════════════════════════════════════
#   ENCABEZADOS Y SEPARADORES
# ═══════════════════════════════════════════════════════════

BANNER = f"""
{c('╔══════════════════════════════════════════════════════╗', Color.CYAN)}
{c('║', Color.CYAN)}  {c('██████╗  ██████╗  ███████╗', Color.AZUL, Color.BOLD)}                          {c('║', Color.CYAN)}
{c('║', Color.CYAN)}  {c('██╔══██╗██╔═══██╗██╔════╝', Color.AZUL, Color.BOLD)}                          {c('║', Color.CYAN)}
{c('║', Color.CYAN)}  {c('██████╔╝██║   ██║███████╗', Color.AZUL, Color.BOLD)}  {c('Sistema Operativo', Color.BLANCO, Color.BOLD)}     {c('║', Color.CYAN)}
{c('║', Color.CYAN)}  {c('██╔═══╝ ██║   ██║╚════██║', Color.AZUL, Color.BOLD)}  {c('Simulado  v1.0', Color.GRIS)}         {c('║', Color.CYAN)}
{c('║', Color.CYAN)}  {c('██║     ╚██████╔╝███████║', Color.AZUL, Color.BOLD)}                          {c('║', Color.CYAN)}
{c('║', Color.CYAN)}  {c('╚═╝      ╚═════╝ ╚══════╝', Color.AZUL, Color.BOLD)}                          {c('║', Color.CYAN)}
{c('╚══════════════════════════════════════════════════════╝', Color.CYAN)}
"""

def separador(titulo="", ancho=56, color=Color.CYAN):
    if titulo:
        pad  = ancho - len(titulo) - 4
        izq  = pad // 2
        der  = pad - izq
        linea = f"{'═' * izq}  {titulo}  {'═' * der}"
    else:
        linea = "═" * ancho
    print(c(f"  {linea}", color))


def titulo_seccion(texto, icono="◈", color=Color.AZUL):
    print()
    print(f"  {c(icono, color, Color.BOLD)}  {c(texto, Color.BLANCO, Color.BOLD)}")
    print(f"  {c('─' * 50, Color.GRIS)}")


def ok(msg):
    print(f"  {c('✓', Color.VERDE, Color.BOLD)}  {c(msg, Color.VERDE)}")

def error(msg):
    print(f"  {c('✗', Color.ROJO, Color.BOLD)}  {c(msg, Color.ROJO)}")

def info(msg):
    print(f"  {c('→', Color.AMARILLO, Color.BOLD)}  {c(msg, Color.AMARILLO)}")

def nota(msg):
    print(f"  {c('·', Color.GRIS)}  {c(msg, Color.GRIS)}")


# ═══════════════════════════════════════════════════════════
#   BADGE DE ESTADO DE PROCESO
# ═══════════════════════════════════════════════════════════

ESTADO_BADGE = {
    "Listo"    : c(" LISTO     ", Color.BG_AZUL,     Color.BLANCO, Color.BOLD),
    "Ejecución": c(" EJECUCIÓN ", Color.BG_AMARILLO, Color.BLANCO, Color.BOLD),
    "Terminado": c(" TERMINADO ", Color.BG_VERDE,    Color.BLANCO, Color.BOLD),
}

def badge_estado(estado):
    return ESTADO_BADGE.get(estado, c(f" {estado} ", Color.BG_NEGRO, Color.BLANCO))


# ═══════════════════════════════════════════════════════════
#   PROCESO SIMULADO
# ═══════════════════════════════════════════════════════════

class Proceso:
    def __init__(self, id_proceso, nombre, tiempo_ejecucion):
        self.id               = id_proceso
        self.nombre           = nombre
        self.tiempo_ejecucion = tiempo_ejecucion
        self.tiempo_restante  = tiempo_ejecucion
        self.estado           = "Listo"
        self.tiempo_inicio    = None
        self.tiempo_fin       = None

    def _cabecera_ejecucion(self, turno):
        print()
        separador(f"TURNO #{turno}", color=Color.AMARILLO)
        print(f"  {c('ID:', Color.GRIS)}  {c(self.id, Color.BLANCO, Color.BOLD)}   "
              f"{c('Proceso:', Color.GRIS)}  {c(self.nombre, Color.MAGENTA, Color.BOLD)}")
        print(f"  {c('Estado:', Color.GRIS)} {badge_estado(self.estado)}")
        print()

    def ejecutar_completo(self, turno=1):
        self.estado       = "Ejecución"
        self.tiempo_inicio = time.time()
        self._cabecera_ejecucion(turno)

        # Barra de progreso animada
        total = self.tiempo_ejecucion
        for paso in range(total + 1):
            barra = barra_progreso(paso, total, color=Color.AMARILLO)
            print(f"\r  {c('CPU', Color.BG_AMARILLO, Color.BG_NEGRO, Color.BOLD)}  {barra}  {c(str(paso) + 's', Color.GRIS)}", end="", flush=True)
            if paso < total:
                time.sleep(1)

        print()
        self.tiempo_restante = 0
        self.estado          = "Terminado"
        self.tiempo_fin      = time.time()
        print(f"\n  {badge_estado(self.estado)}  {c(self.nombre, Color.BLANCO, Color.BOLD)}")

    def ejecutar_por_quantum(self, quantum, turno=1):
        self.estado        = "Ejecución"
        if self.tiempo_inicio is None:
            self.tiempo_inicio = time.time()

        tiempo_a_ejecutar = min(quantum, self.tiempo_restante)
        self._cabecera_ejecucion(turno)

        print(f"  {c('Quantum:', Color.GRIS)}       {c(str(quantum) + 's', Color.BLANCO, Color.BOLD)}")
        print(f"  {c('Tiempo restante:', Color.GRIS)} {c(str(self.tiempo_restante) + 's', Color.BLANCO, Color.BOLD)}")
        print(f"  {c('Este turno:', Color.GRIS)}     {c(str(tiempo_a_ejecutar) + 's', Color.AMARILLO, Color.BOLD)}")
        print()

        for paso in range(tiempo_a_ejecutar + 1):
            barra = barra_progreso(paso, tiempo_a_ejecutar, color=Color.MAGENTA)
            print(f"\r  {c('CPU', Color.BG_MAGENTA, Color.BLANCO, Color.BOLD)}  {barra}  {c(str(paso) + 's', Color.GRIS)}", end="", flush=True)
            if paso < tiempo_a_ejecutar:
                time.sleep(1)

        print()
        self.tiempo_restante -= tiempo_a_ejecutar

        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0
            self.estado          = "Terminado"
            self.tiempo_fin      = time.time()
            print(f"\n  {badge_estado(self.estado)}  {c(self.nombre, Color.BLANCO, Color.BOLD)}")
        else:
            self.estado = "Listo"
            info(f"Vuelve a la cola  ·  Tiempo restante: {c(str(self.tiempo_restante) + 's', Color.AMARILLO, Color.BOLD)}")
            print(f"  {badge_estado(self.estado)}")


# ═══════════════════════════════════════════════════════════
#   PLANIFICADOR
# ═══════════════════════════════════════════════════════════

ALGORITMOS = {
    "1": "FIFO",
    "2": "SJF",
    "3": "ROUND ROBIN",
}

ALGORITMO_DESC = {
    "FIFO"        : "First In, First Out — orden de llegada",
    "SJF"         : "Shortest Job First — menor tiempo primero",
    "ROUND ROBIN" : "Round Robin — turnos por quantum",
}

ALGORITMO_COLOR = {
    "FIFO"        : Color.AZUL,
    "SJF"         : Color.VERDE,
    "ROUND ROBIN" : Color.MAGENTA,
}


class Planificador:
    def __init__(self):
        self.procesos          = []
        self.procesos_ejecutados = []
        self.algoritmo         = "FIFO"
        self.historial         = []   # registro de ejecución para el resumen

    # ── Gestión de procesos ───────────────────────────────

    def agregar_proceso(self, proceso):
        if self.buscar_proceso(proceso.id) is not None:
            error(f"Ya existe un proceso con ID  '{proceso.id}'")
            return False
        self.procesos.append(proceso)
        ok(f"Proceso agregado  ·  {c(proceso.id, Color.BLANCO, Color.BOLD)} — {proceso.nombre}  ·  {proceso.tiempo_ejecucion}s")
        print(f"     Estado inicial: {badge_estado(proceso.estado)}")
        return True

    def buscar_proceso(self, id_proceso):
        for p in self.procesos + self.procesos_ejecutados:
            if p.id == id_proceso:
                return p
        return None

    def existe_proceso(self, id_proceso):
        return self.buscar_proceso(id_proceso) is not None

    # ── Selección de algoritmo ────────────────────────────

    def seleccionar_algoritmo(self, clave):
        nombre = ALGORITMOS.get(clave)
        if not nombre:
            error("Opción de algoritmo no válida.")
            return False
        self.algoritmo = nombre
        color = ALGORITMO_COLOR[nombre]
        ok(f"Algoritmo activo: {c(nombre, color, Color.BOLD)}  ·  {c(ALGORITMO_DESC[nombre], Color.GRIS)}")
        return True

    # ── Visualización ─────────────────────────────────────

    def mostrar_procesos(self):
        titulo_seccion("LISTA DE PROCESOS", "⚙", Color.AZUL)

        if not self.procesos and not self.procesos_ejecutados:
            nota("No hay procesos registrados.")
            return

        if self.procesos:
            print(f"  {c('PENDIENTES', Color.AMARILLO, Color.BOLD)}")
            print()
            # cabecera tabla
            print(f"  {c('ID        NOMBRE            TIEMPO TOTAL  RESTANTE  ESTADO', Color.GRIS)}")
            print(f"  {c('─' * 60, Color.GRIS)}")
            for p in self.procesos:
                barra = barra_progreso(
                    p.tiempo_ejecucion - p.tiempo_restante,
                    p.tiempo_ejecucion, ancho=10, color=Color.AZUL
                )
                print(
                    f"  {c(p.id.ljust(10), Color.CYAN)}",
                    f"{c(p.nombre.ljust(18), Color.BLANCO)}",
                    f"{c(str(p.tiempo_ejecucion).ljust(4) + 's', Color.AMARILLO)}",
                    f"      {c(str(p.tiempo_restante).ljust(4) + 's', Color.BLANCO)}",
                    f"  {badge_estado(p.estado)}"
                )
        else:
            nota("Sin procesos pendientes.")

        print()
        if self.procesos_ejecutados:
            print(f"  {c('COMPLETADOS', Color.VERDE, Color.BOLD)}")
            print()
            print(f"  {c('ID        NOMBRE            ESTADO', Color.GRIS)}")
            print(f"  {c('─' * 42, Color.GRIS)}")
            for p in self.procesos_ejecutados:
                print(
                    f"  {c(p.id.ljust(10), Color.CYAN)}",
                    f"{c(p.nombre.ljust(18), Color.BLANCO)}",
                    f"  {badge_estado(p.estado)}"
                )

    # ── Ejecución ─────────────────────────────────────────

    def ejecutar(self):
        if not self.procesos:
            error("No hay procesos pendientes en la cola.")
            return

        color_alg = ALGORITMO_COLOR[self.algoritmo]
        print()
        separador("PLANIFICADOR DE CPU", color=color_alg)
        print(f"  {c('Algoritmo:', Color.GRIS)}  {c(self.algoritmo, color_alg, Color.BOLD)}  ·  {c(ALGORITMO_DESC[self.algoritmo], Color.GRIS)}")
        print(f"  {c('Procesos en cola:', Color.GRIS)}  {c(str(len(self.procesos)), Color.BLANCO, Color.BOLD)}")
        separador(color=color_alg)

        self.historial = []
        t_inicio_global = time.time()

        if   self.algoritmo == "FIFO":
            self._ejecutar_fifo()
        elif self.algoritmo == "SJF":
            self._ejecutar_sjf()
        elif self.algoritmo == "ROUND ROBIN":
            self._ejecutar_round_robin()

        t_total = round(time.time() - t_inicio_global, 1)
        self._resumen_ejecucion(t_total)

    def _ejecutar_fifo(self):
        info("Orden: primero en llegar, primero en ejecutarse.")
        turno = 1
        while self.procesos:
            p = self.procesos.pop(0)
            p.ejecutar_completo(turno)
            self.procesos_ejecutados.append(p)
            self.historial.append((turno, p))
            turno += 1

    def _ejecutar_sjf(self):
        info("Ordenando procesos por menor tiempo de ejecución…")
        self.procesos.sort(key=lambda p: p.tiempo_ejecucion)
        animar_carga("Reorganizando cola", 0.6)
        print()
        # Mostrar el orden resultante
        print(f"  {c('Orden de ejecución:', Color.GRIS)}")
        for i, p in enumerate(self.procesos, 1):
            print(f"    {c(str(i) + '.', Color.GRIS)}  {c(p.nombre, Color.BLANCO, Color.BOLD)}  {c('(' + str(p.tiempo_ejecucion) + 's)', Color.AMARILLO)}")
        print()

        turno = 1
        while self.procesos:
            p = self.procesos.pop(0)
            p.ejecutar_completo(turno)
            self.procesos_ejecutados.append(p)
            self.historial.append((turno, p))
            turno += 1

    def _ejecutar_round_robin(self):
        print()
        quantum = pedir_entero(
            f"  {c('▸', Color.MAGENTA, Color.BOLD)}  Quantum en segundos: ",
            minimo=1
        )
        if quantum is None:
            return

        info(f"Quantum asignado: {c(str(quantum) + 's', Color.MAGENTA, Color.BOLD)}")
        print()

        turno = 1
        while self.procesos:
            p = self.procesos.pop(0)
            p.ejecutar_por_quantum(quantum, turno)

            if p.estado == "Terminado":
                self.procesos_ejecutados.append(p)
                self.historial.append((turno, p))
            else:
                self.procesos.append(p)

            turno += 1

    # ── Resumen final de ejecución ────────────────────────

    def _resumen_ejecucion(self, t_total):
        print()
        separador("RESUMEN DE EJECUCIÓN", color=Color.VERDE)

        print(f"  {c('Algoritmo usado:', Color.GRIS)}   {c(self.algoritmo, ALGORITMO_COLOR[self.algoritmo], Color.BOLD)}")
        print(f"  {c('Procesos completados:', Color.GRIS)} {c(str(len(self.procesos_ejecutados)), Color.VERDE, Color.BOLD)}")
        print(f"  {c('Tiempo total CPU:', Color.GRIS)}  {c(str(t_total) + 's', Color.AMARILLO, Color.BOLD)}")
        print()

        print(f"  {c('ORDEN DE FINALIZACIÓN', Color.BLANCO, Color.BOLD)}")
        print()
        print(f"  {c('Turno  ID          Nombre              Tiempo', Color.GRIS)}")
        print(f"  {c('─' * 52, Color.GRIS)}")

        for i, (turno, p) in enumerate(self.historial):
            indicador = c("►", Color.VERDE)
            print(f"  {indicador}  {c(str(turno).ljust(5), Color.AMARILLO)}  {c(p.id.ljust(10), Color.CYAN)}  {c(p.nombre.ljust(18), Color.BLANCO)}  {c(str(p.tiempo_ejecucion) + 's', Color.AMARILLO)}")

        separador(color=Color.VERDE)
        print(f"  {c('✓', Color.VERDE, Color.BOLD)}  Todos los procesos han finalizado correctamente.")


# ═══════════════════════════════════════════════════════════
#   MEMORIA
# ═══════════════════════════════════════════════════════════

class Memoria:
    def __init__(self, memoria_total=1024):
        self.memoria_total = memoria_total
        self.memoria_usada = 0
        self.asignaciones  = {}   # id → tamaño

    # ── Propiedades ───────────────────────────────────────

    @property
    def memoria_libre(self):
        return self.memoria_total - self.memoria_usada

    @property
    def porcentaje_uso(self):
        return self.memoria_usada / self.memoria_total

    # ── Operaciones ───────────────────────────────────────

    def asignar(self, id_proceso, tamaño, planificador):
        if not planificador.existe_proceso(id_proceso):
            error(f"No existe proceso con ID '{id_proceso}'.")
            nota("Crea el proceso primero desde la opción 1.")
            return False
        if id_proceso in self.asignaciones:
            error(f"El proceso '{id_proceso}' ya tiene memoria asignada ({self.asignaciones[id_proceso]} MB).")
            nota("Libera la memoria existente antes de reasignar.")
            return False
        if tamaño <= 0:
            error("El tamaño debe ser mayor que 0 MB.")
            return False
        if tamaño > self.memoria_libre:
            error(f"Memoria insuficiente.  Solicitado: {tamaño} MB  ·  Disponible: {self.memoria_libre} MB")
            self.mostrar_estado()
            return False

        self.asignaciones[id_proceso] = tamaño
        self.memoria_usada += tamaño
        ok(f"Asignados {c(str(tamaño) + ' MB', Color.VERDE, Color.BOLD)} al proceso {c(id_proceso, Color.CYAN, Color.BOLD)}")
        self.mostrar_estado()
        return True

    def liberar(self, id_proceso):
        if id_proceso not in self.asignaciones:
            error(f"No hay memoria asignada al proceso '{id_proceso}'.")
            return False
        tamaño = self.asignaciones.pop(id_proceso)
        self.memoria_usada -= tamaño
        ok(f"Liberados {c(str(tamaño) + ' MB', Color.VERDE, Color.BOLD)} del proceso {c(id_proceso, Color.CYAN, Color.BOLD)}")
        self.mostrar_estado()
        return True

    # ── Visualización ─────────────────────────────────────

    def mostrar_estado(self):
        titulo_seccion("ESTADO DE MEMORIA", "▣", Color.MAGENTA)

        # Barra visual global
        barra = barra_progreso(self.memoria_usada, self.memoria_total, ancho=36, color=Color.MAGENTA)
        print(f"  {barra}")
        print()
        print(f"  {c('Total:     ', Color.GRIS)} {c(str(self.memoria_total) + ' MB', Color.BLANCO, Color.BOLD)}")
        print(f"  {c('En uso:    ', Color.GRIS)} {c(str(self.memoria_usada) + ' MB', Color.MAGENTA, Color.BOLD)}")
        print(f"  {c('Disponible:', Color.GRIS)} {c(str(self.memoria_libre) + ' MB', Color.VERDE, Color.BOLD)}")

        if not self.asignaciones:
            print()
            nota("No hay procesos con memoria asignada.")
            return

        print()
        print(f"  {c('ASIGNACIONES ACTIVAS', Color.BLANCO, Color.BOLD)}")
        print()
        print(f"  {c('Proceso     Asignado   % del total', Color.GRIS)}")
        print(f"  {c('─' * 40, Color.GRIS)}")

        for id_p, tam in self.asignaciones.items():
            pct     = int((tam / self.memoria_total) * 100)
            mini    = barra_progreso(tam, self.memoria_total, ancho=14, color=Color.MAGENTA)
            print(f"  {c(id_p.ljust(12), Color.CYAN)}{c(str(tam).rjust(4) + ' MB', Color.BLANCO, Color.BOLD)}   {mini}  {c(str(pct) + '%', Color.GRIS)}")


# ═══════════════════════════════════════════════════════════
#   MODO DEMO
# ═══════════════════════════════════════════════════════════

def cargar_demo(planificador, memoria):
    titulo_seccion("CARGANDO DATOS DE PRUEBA", "▶", Color.CYAN)
    info("Creando 3 procesos de ejemplo…")
    print()

    demos = [
        ("P001", "Sistema de Archivos", 4),
        ("P002", "Gestor de Red",       2),
        ("P003", "Monitor del Sistema", 6),
    ]
    for id_p, nombre, tiempo in demos:
        p = Proceso(id_p, nombre, tiempo)
        planificador.agregar_proceso(p)
        time.sleep(0.15)

    print()
    info("Asignando memoria de ejemplo…")
    print()
    memoria.asignar("P001", 128, planificador)
    time.sleep(0.1)
    memoria.asignar("P002",  64, planificador)
    time.sleep(0.1)
    memoria.asignar("P003", 256, planificador)

    print()
    ok("Demo cargado. Ya puedes ejecutar los procesos (opción 7).")


# ═══════════════════════════════════════════════════════════
#   FUNCIONES AUXILIARES DE ENTRADA
# ═══════════════════════════════════════════════════════════

def pedir_entero(mensaje, minimo=None, maximo=None):
    try:
        valor = int(input(mensaje))
    except ValueError:
        error("Debes ingresar un número entero.")
        return None
    if minimo is not None and valor < minimo:
        error(f"El valor mínimo es {minimo}.")
        return None
    if maximo is not None and valor > maximo:
        error(f"El valor máximo es {maximo}.")
        return None
    return valor


def pedir_texto(mensaje):
    valor = input(mensaje).strip()
    if not valor:
        error("El campo no puede estar vacío.")
        return None
    return valor


# ═══════════════════════════════════════════════════════════
#   MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def mostrar_menu(planificador):
    alg   = planificador.algoritmo
    color = ALGORITMO_COLOR[alg]
    pend  = len(planificador.procesos)
    comp  = len(planificador.procesos_ejecutados)

    print(BANNER)
    separador()

    # Barra de estado rápida
    print(f"  {c('Algoritmo:', Color.GRIS)}  {c(alg, color, Color.BOLD)}   "
          f"{c('En cola:', Color.GRIS)}  {c(str(pend), Color.AMARILLO, Color.BOLD)}   "
          f"{c('Completados:', Color.GRIS)}  {c(str(comp), Color.VERDE, Color.BOLD)}")
    separador()
    print()

    opciones = [
        ("0", "Cargar demo de prueba",            Color.GRIS),
        ("1", "Crear proceso",                    Color.CYAN),
        ("2", "Ver lista de procesos",            Color.CYAN),
        ("3", "Asignar memoria a proceso",        Color.MAGENTA),
        ("4", "Liberar memoria de proceso",       Color.MAGENTA),
        ("5", "Ver estado de memoria",            Color.MAGENTA),
        ("6", "Seleccionar algoritmo de planif.", Color.AZUL),
        ("7", "Ejecutar todos los procesos",      Color.AMARILLO),
        ("8", "Salir",                            Color.ROJO),
    ]
    for num, desc, col in opciones:
        flecha = c("▸", col, Color.BOLD)
        num_fmt = c(f"[{num}]", col, Color.BOLD)
        print(f"   {flecha}  {num_fmt}  {c(desc, Color.BLANCO)}")

    print()
    separador()


def mostrar_menu_algoritmos():
    titulo_seccion("ALGORITMO DE PLANIFICACIÓN", "⚙", Color.AZUL)

    datos = [
        ("1", "FIFO",         "First In, First Out",     "Orden de llegada",          Color.AZUL),
        ("2", "SJF",          "Shortest Job First",      "Menor tiempo primero",       Color.VERDE),
        ("3", "ROUND ROBIN",  "Round Robin",             "Turnos por quantum",         Color.MAGENTA),
    ]
    for num, sig, nombre, desc, col in datos:
        num_fmt = c(f"[{num}]", col, Color.BOLD)
        sig_fmt = c(sig.ljust(12), col, Color.BOLD)
        print(f"   {num_fmt}  {sig_fmt}  {c(nombre, Color.BLANCO)}  {c('·', Color.GRIS)}  {c(desc, Color.GRIS)}")
    print()


# ═══════════════════════════════════════════════════════════
#   INTERFAZ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def interfaz_usuario():
    planificador = Planificador()
    memoria      = Memoria(memoria_total=1024)

    limpiar()
    print(BANNER)
    animar_carga("Iniciando núcleo del sistema", 1.0)
    animar_carga("Cargando gestor de procesos", 0.6)
    animar_carga("Inicializando memoria RAM (1024 MB)", 0.6)
    print()
    ok("Sistema operativo listo.")
    time.sleep(0.5)

    while True:
        limpiar()
        mostrar_menu(planificador)

        opcion = input(f"  {c('▸', Color.AMARILLO, Color.BOLD)}  Selecciona una opción: ").strip()

        # ── DEMO ──────────────────────────────────────────
        if opcion == "0":
            limpiar()
            cargar_demo(planificador, memoria)

        # ── CREAR PROCESO ─────────────────────────────────
        elif opcion == "1":
            limpiar()
            titulo_seccion("CREAR PROCESO", "✦", Color.CYAN)

            id_p   = pedir_texto(f"  {c('▸', Color.CYAN)}  ID del proceso:     ")
            if id_p is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            nombre = pedir_texto(f"  {c('▸', Color.CYAN)}  Nombre del proceso: ")
            if nombre is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            tiempo = pedir_entero(
                f"  {c('▸', Color.CYAN)}  Tiempo de ejecución (seg): ",
                minimo=1, maximo=60
            )
            if tiempo is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            print()
            animar_carga("Registrando proceso", 0.4)
            p = Proceso(id_p, nombre, tiempo)
            planificador.agregar_proceso(p)

        # ── VER PROCESOS ──────────────────────────────────
        elif opcion == "2":
            limpiar()
            planificador.mostrar_procesos()

        # ── ASIGNAR MEMORIA ───────────────────────────────
        elif opcion == "3":
            limpiar()
            titulo_seccion("ASIGNAR MEMORIA", "▣", Color.MAGENTA)

            id_p  = pedir_texto(f"  {c('▸', Color.MAGENTA)}  ID del proceso:         ")
            if id_p is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            tamaño = pedir_entero(
                f"  {c('▸', Color.MAGENTA)}  Tamaño a asignar (MB):  ",
                minimo=1, maximo=memoria.memoria_total
            )
            if tamaño is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            print()
            memoria.asignar(id_p, tamaño, planificador)

        # ── LIBERAR MEMORIA ───────────────────────────────
        elif opcion == "4":
            limpiar()
            titulo_seccion("LIBERAR MEMORIA", "▣", Color.MAGENTA)

            id_p = pedir_texto(f"  {c('▸', Color.MAGENTA)}  ID del proceso: ")
            if id_p is None:
                input(f"\n  {c('Presiona Enter para continuar...', Color.GRIS)}")
                continue

            print()
            memoria.liberar(id_p)

        # ── VER MEMORIA ───────────────────────────────────
        elif opcion == "5":
            limpiar()
            memoria.mostrar_estado()

        # ── SELECCIONAR ALGORITMO ─────────────────────────
        elif opcion == "6":
            limpiar()
            mostrar_menu_algoritmos()
            clave = input(f"  {c('▸', Color.AZUL, Color.BOLD)}  Selecciona algoritmo [1/2/3]: ").strip()
            print()
            planificador.seleccionar_algoritmo(clave)

        # ── EJECUTAR PROCESOS ─────────────────────────────
        elif opcion == "7":
            limpiar()
            planificador.ejecutar()

        # ── SALIR ─────────────────────────────────────────
        elif opcion == "8":
            limpiar()
            separador("APAGANDO SISTEMA", color=Color.ROJO)
            animar_carga("Finalizando procesos activos", 0.5)
            animar_carga("Liberando memoria del sistema", 0.4)
            animar_carga("Guardando registros",           0.3)
            print()
            print(f"  {c('✓', Color.VERDE, Color.BOLD)}  Sistema operativo detenido correctamente.")
            print()
            separador(color=Color.ROJO)
            print()
            sys.exit(0)

        else:
            error("Opción no válida. Elige una opción del menú.")

        print()
        input(f"  {c('Presiona Enter para continuar...', Color.GRIS)}")


# ═══════════════════════════════════════════════════════════
#   PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        interfaz_usuario()
    except KeyboardInterrupt:
        print(f"\n\n  {c('Sistema interrumpido por el usuario.', Color.AMARILLO)}\n")
        sys.exit(0)