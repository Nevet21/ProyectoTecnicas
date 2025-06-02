from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.HistorialService import HistorialService
from Proyecto.CRUD_Entidades.JuegoService import JuegoService
from Proyecto.Busquedas_y_ordenamientos.Ordenamientos import burbuja, seleccion, insercion
from Proyecto.Busquedas_y_ordenamientos.Busquedas import busquedaLineal, busquedaBinaria

class ReporteCasino:

    def __init__(self, jugador_service: JugadorService, historial_service: HistorialService, juego_service: JuegoService):
        self.jugador_service = jugador_service
        self.historial_service = historial_service
        self.juego_service = juego_service

    def jugadores_mayor_saldo(self):
        players = self.jugador_service.obtener_jugadores()
        sorted_players = burbuja(players, "saldo")
        print("\n--- Players with the Highest Balance ---")
        for j in sorted_players[:10]:
            print(f"{j.nombre} - ${j.saldo}")

    def historial_jugador(self):
        player_id = input("Enter the player ID: ").strip()
        found = 0
        print(f"\n=== PLAYER HISTORY {player_id} ===")
        for history in self.historial_service.historiales:
            result = history.get_resultado()
            if result and "jugadores" in result and player_id in result["jugadores"]:
                history.mostrar_info()
                found += 1
                print("-" * 50)
        if found == 0:
            print("No history found for that player.")

    def jugadores_mas_victorias(self):
        players = self.jugador_service.obtener_jugadores()
        sorted_players = insercion(players, "juegos_ganados")
        print("\n--- Players with the Most Wins ---")
        for j in sorted_players[:10]:
            print(f"{j.nombre} - {j.juegos_ganados} wins")

    def jugadores_con_mas_perdidas(self):
        players = self.jugador_service.obtener_jugadores()
        sorted_players = seleccion(players, "juegos_perdidos")
        print("\n--- Players with the Most Losses ---")
        for j in sorted_players[:10]:
            print(f"{j.nombre} - {j.juegos_perdidos} losses")

    def juegos_mas_participados(self):
        count = {}
        for h in self.historial_service.historiales:
            try:
                table = h.get_mesa()
                if table and table.juego:
                    game_name = table.juego.get_nombre()
                    count[game_name] = count.get(game_name, 0) + 1
            except AttributeError:
                continue  # Skip if data is missing
        print("\n--- Most Participated Games ---")
        for game, total in sorted(count.items(), key=lambda x: x[1], reverse=True):
            print(f"{game}: {total} participations")

