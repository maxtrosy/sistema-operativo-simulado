import unittest
from unittest.mock import patch

from main import Proceso, Planificador, Memoria, badge_estado, cargar_demo


class TestProceso(unittest.TestCase):

    def test_crear_proceso(self):
        proceso = Proceso("P001", "Sistema de Archivos", 4)

        self.assertEqual(proceso.id, "P001")
        self.assertEqual(proceso.nombre, "Sistema de Archivos")
        self.assertEqual(proceso.tiempo_ejecucion, 4)
        self.assertEqual(proceso.tiempo_restante, 4)
        self.assertEqual(proceso.estado, "Listo")
        self.assertIsNone(proceso.tiempo_inicio)
        self.assertIsNone(proceso.tiempo_fin)

    @patch("main.time.sleep", return_value=None)
    def test_ejecutar_completo_termina_proceso(self, mock_sleep):
        proceso = Proceso("P001", "Proceso Test", 2)

        proceso.ejecutar_completo(turno=1)

        self.assertEqual(proceso.estado, "Terminado")
        self.assertEqual(proceso.tiempo_restante, 0)
        self.assertIsNotNone(proceso.tiempo_inicio)
        self.assertIsNotNone(proceso.tiempo_fin)

    @patch("main.time.sleep", return_value=None)
    def test_ejecutar_por_quantum_no_termina_si_falta_tiempo(self, mock_sleep):
        proceso = Proceso("P001", "Proceso Test", 5)

        proceso.ejecutar_por_quantum(quantum=2, turno=1)

        self.assertEqual(proceso.estado, "Listo")
        self.assertEqual(proceso.tiempo_restante, 3)
        self.assertIsNotNone(proceso.tiempo_inicio)
        self.assertIsNone(proceso.tiempo_fin)

    @patch("main.time.sleep", return_value=None)
    def test_ejecutar_por_quantum_termina_si_quantum_alcanza(self, mock_sleep):
        proceso = Proceso("P001", "Proceso Test", 2)

        proceso.ejecutar_por_quantum(quantum=5, turno=1)

        self.assertEqual(proceso.estado, "Terminado")
        self.assertEqual(proceso.tiempo_restante, 0)
        self.assertIsNotNone(proceso.tiempo_inicio)
        self.assertIsNotNone(proceso.tiempo_fin)


class TestPlanificador(unittest.TestCase):

    def test_estado_inicial_planificador(self):
        planificador = Planificador()

        self.assertEqual(planificador.procesos, [])
        self.assertEqual(planificador.procesos_ejecutados, [])
        self.assertEqual(planificador.algoritmo, "FIFO")
        self.assertEqual(planificador.historial, [])

    def test_agregar_proceso_correctamente(self):
        planificador = Planificador()
        proceso = Proceso("P001", "Calculadora", 3)

        resultado = planificador.agregar_proceso(proceso)

        self.assertTrue(resultado)
        self.assertEqual(len(planificador.procesos), 1)
        self.assertEqual(planificador.procesos[0].id, "P001")

    def test_no_permite_proceso_duplicado(self):
        planificador = Planificador()

        proceso1 = Proceso("P001", "Calculadora", 3)
        proceso2 = Proceso("P001", "Navegador", 4)

        resultado1 = planificador.agregar_proceso(proceso1)
        resultado2 = planificador.agregar_proceso(proceso2)

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)
        self.assertEqual(len(planificador.procesos), 1)

    def test_buscar_proceso_existente(self):
        planificador = Planificador()
        proceso = Proceso("P001", "Calculadora", 3)

        planificador.agregar_proceso(proceso)
        encontrado = planificador.buscar_proceso("P001")

        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Calculadora")

    def test_buscar_proceso_inexistente(self):
        planificador = Planificador()

        encontrado = planificador.buscar_proceso("P999")

        self.assertIsNone(encontrado)

    def test_existe_proceso(self):
        planificador = Planificador()
        proceso = Proceso("P001", "Calculadora", 3)

        planificador.agregar_proceso(proceso)

        self.assertTrue(planificador.existe_proceso("P001"))
        self.assertFalse(planificador.existe_proceso("P999"))

    def test_seleccionar_fifo(self):
        planificador = Planificador()

        resultado = planificador.seleccionar_algoritmo("1")

        self.assertTrue(resultado)
        self.assertEqual(planificador.algoritmo, "FIFO")

    def test_seleccionar_sjf(self):
        planificador = Planificador()

        resultado = planificador.seleccionar_algoritmo("2")

        self.assertTrue(resultado)
        self.assertEqual(planificador.algoritmo, "SJF")

    def test_seleccionar_round_robin(self):
        planificador = Planificador()

        resultado = planificador.seleccionar_algoritmo("3")

        self.assertTrue(resultado)
        self.assertEqual(planificador.algoritmo, "ROUND ROBIN")

    def test_seleccionar_algoritmo_invalido(self):
        planificador = Planificador()

        resultado = planificador.seleccionar_algoritmo("9")

        self.assertFalse(resultado)
        self.assertEqual(planificador.algoritmo, "FIFO")

    @patch("main.time.sleep", return_value=None)
    def test_ejecucion_fifo_respeta_orden_llegada(self, mock_sleep):
        planificador = Planificador()

        p1 = Proceso("P001", "Proceso 1", 1)
        p2 = Proceso("P002", "Proceso 2", 1)
        p3 = Proceso("P003", "Proceso 3", 1)

        planificador.agregar_proceso(p1)
        planificador.agregar_proceso(p2)
        planificador.agregar_proceso(p3)

        planificador.seleccionar_algoritmo("1")
        planificador.ejecutar()

        orden = [p.id for p in planificador.procesos_ejecutados]

        self.assertEqual(orden, ["P001", "P002", "P003"])
        self.assertEqual(len(planificador.procesos), 0)
        self.assertEqual(len(planificador.procesos_ejecutados), 3)

    @patch("main.time.sleep", return_value=None)
    def test_ejecucion_sjf_ordena_por_menor_tiempo(self, mock_sleep):
        planificador = Planificador()

        p1 = Proceso("P001", "Proceso Largo", 5)
        p2 = Proceso("P002", "Proceso Corto", 1)
        p3 = Proceso("P003", "Proceso Medio", 3)

        planificador.agregar_proceso(p1)
        planificador.agregar_proceso(p2)
        planificador.agregar_proceso(p3)

        planificador.seleccionar_algoritmo("2")
        planificador.ejecutar()

        orden = [p.id for p in planificador.procesos_ejecutados]

        self.assertEqual(orden, ["P002", "P003", "P001"])
        self.assertEqual(len(planificador.procesos), 0)
        self.assertEqual(len(planificador.procesos_ejecutados), 3)

    @patch("main.time.sleep", return_value=None)
    @patch("builtins.input", return_value="2")
    def test_ejecucion_round_robin_termina_todos_los_procesos(self, mock_input, mock_sleep):
        planificador = Planificador()

        p1 = Proceso("P001", "Proceso 1", 5)
        p2 = Proceso("P002", "Proceso 2", 3)

        planificador.agregar_proceso(p1)
        planificador.agregar_proceso(p2)

        planificador.seleccionar_algoritmo("3")
        planificador.ejecutar()

        self.assertEqual(len(planificador.procesos), 0)
        self.assertEqual(len(planificador.procesos_ejecutados), 2)

        for proceso in planificador.procesos_ejecutados:
            self.assertEqual(proceso.estado, "Terminado")
            self.assertEqual(proceso.tiempo_restante, 0)


class TestMemoria(unittest.TestCase):

    def test_estado_inicial_memoria(self):
        memoria = Memoria(memoria_total=1024)

        self.assertEqual(memoria.memoria_total, 1024)
        self.assertEqual(memoria.memoria_usada, 0)
        self.assertEqual(memoria.memoria_libre, 1024)
        self.assertEqual(memoria.asignaciones, {})

    def test_porcentaje_uso_memoria(self):
        memoria = Memoria(memoria_total=1000)
        memoria.memoria_usada = 250

        self.assertEqual(memoria.porcentaje_uso, 0.25)

    def test_asignar_memoria_correctamente(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        resultado = memoria.asignar("P001", 200, planificador)

        self.assertTrue(resultado)
        self.assertEqual(memoria.asignaciones["P001"], 200)
        self.assertEqual(memoria.memoria_usada, 200)
        self.assertEqual(memoria.memoria_libre, 824)

    def test_no_asignar_memoria_a_proceso_inexistente(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        resultado = memoria.asignar("P999", 200, planificador)

        self.assertFalse(resultado)
        self.assertEqual(memoria.memoria_usada, 0)
        self.assertEqual(memoria.asignaciones, {})

    def test_no_asignar_memoria_duplicada(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        resultado1 = memoria.asignar("P001", 200, planificador)
        resultado2 = memoria.asignar("P001", 300, planificador)

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)
        self.assertEqual(memoria.asignaciones["P001"], 200)
        self.assertEqual(memoria.memoria_usada, 200)

    def test_no_asignar_memoria_negativa(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        resultado = memoria.asignar("P001", -100, planificador)

        self.assertFalse(resultado)
        self.assertEqual(memoria.memoria_usada, 0)
        self.assertNotIn("P001", memoria.asignaciones)

    def test_no_asignar_memoria_cero(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        resultado = memoria.asignar("P001", 0, planificador)

        self.assertFalse(resultado)
        self.assertEqual(memoria.memoria_usada, 0)

    def test_no_asignar_memoria_excesiva(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        resultado = memoria.asignar("P001", 2000, planificador)

        self.assertFalse(resultado)
        self.assertEqual(memoria.memoria_usada, 0)
        self.assertEqual(memoria.memoria_libre, 1024)

    def test_liberar_memoria_correctamente(self):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        proceso = Proceso("P001", "Calculadora", 3)
        planificador.agregar_proceso(proceso)

        memoria.asignar("P001", 200, planificador)
        resultado = memoria.liberar("P001")

        self.assertTrue(resultado)
        self.assertEqual(memoria.memoria_usada, 0)
        self.assertEqual(memoria.memoria_libre, 1024)
        self.assertNotIn("P001", memoria.asignaciones)

    def test_no_liberar_memoria_inexistente(self):
        memoria = Memoria(memoria_total=1024)

        resultado = memoria.liberar("P999")

        self.assertFalse(resultado)


class TestFuncionesAuxiliares(unittest.TestCase):

    def test_badge_estado_listo(self):
        resultado = badge_estado("Listo")

        self.assertIn("LISTO", resultado)

    def test_badge_estado_ejecucion(self):
        resultado = badge_estado("Ejecución")

        self.assertIn("EJECUCIÓN", resultado)

    def test_badge_estado_terminado(self):
        resultado = badge_estado("Terminado")

        self.assertIn("TERMINADO", resultado)

    def test_badge_estado_desconocido(self):
        resultado = badge_estado("Suspendido")

        self.assertIn("Suspendido", resultado)

    @patch("main.time.sleep", return_value=None)
    def test_cargar_demo_crea_tres_procesos_y_asigna_memoria(self, mock_sleep):
        planificador = Planificador()
        memoria = Memoria(memoria_total=1024)

        cargar_demo(planificador, memoria)

        self.assertEqual(len(planificador.procesos), 3)
        self.assertTrue(planificador.existe_proceso("P001"))
        self.assertTrue(planificador.existe_proceso("P002"))
        self.assertTrue(planificador.existe_proceso("P003"))

        self.assertEqual(memoria.asignaciones["P001"], 128)
        self.assertEqual(memoria.asignaciones["P002"], 64)
        self.assertEqual(memoria.asignaciones["P003"], 256)
        self.assertEqual(memoria.memoria_usada, 448)


if __name__ == "__main__":
    unittest.main()