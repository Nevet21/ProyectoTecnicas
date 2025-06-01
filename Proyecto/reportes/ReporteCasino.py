from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.HistorialService import HistorialService
from Proyecto.CRUD_Entidades.JuegoService import JuegoService
from Proyecto.Busquedas_y_ordenamientos.Ordenamientos import burbuja, seleccion, insercion

class ReporteCasino:

    def __init__(self, jugador_service: JugadorService, historial_service: HistorialService, juego_service: JuegoService):
        self.jugador_service = jugador_service
        self.historial_service = historial_service
        self.juego_service = juego_service

    def jugadores_mayor_saldo(self):
        jugadores = self.jugador_service.obtener_jugadores()
        ordenados = burbuja(jugadores, "saldo")
        print("\n--- Jugadores con mayor saldo ---")
        for j in ordenados[:10]:
            print(f"{j.nombre} - ${j.saldo}")

    def historial_jugador(self):
        jugador_id = input("Ingrese el ID del jugador: ").strip()
        encontrados = 0
        print(f"\n=== HISTORIAL DEL JUGADOR {jugador_id} ===")
        for historial in self.historial_service.historiales:
            resultado = historial.get_resultado()
            if resultado and "jugadores" in resultado and jugador_id in resultado["jugadores"]:
                historial.mostrar_info()
                encontrados += 1
                print("-" * 50)
        if encontrados == 0:
            print("No se encontró historial para ese jugador.")

    def jugadores_mas_victorias(self):
        jugadores = self.jugador_service.obtener_jugadores()
        ordenados = insercion(jugadores, "juegos_ganados")
        print("\n--- Jugadores con más victorias ---")
        for j in ordenados[:10]:
            print(f"{j.nombre} - {j.juegos_ganados} victorias")

    def jugadores_con_mas_perdidas(self):
        jugadores = self.jugador_service.obtener_jugadores()
        ordenados = seleccion(jugadores, "juegos_perdidos")
        print("\n--- Jugadores con más derrotas ---")
        for j in ordenados[:10]:
            print(f"{j.nombre} - {j.juegos_perdidos} derrotas")

    def juegos_mas_participados(self):
        conteo = {}
        for h in self.historial_service.historiales:
            try:
                mesa = h.get_mesa()
                if mesa and mesa.juego:
                    nombre_juego = mesa.juego.get_nombre()
                    conteo[nombre_juego] = conteo.get(nombre_juego, 0) + 1
            except AttributeError:
                continue  # Saltar si falta información
        print("\n--- Juegos con más participaciones ---")
        for juego, total in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
            print(f"{juego}: {total} participaciones")
