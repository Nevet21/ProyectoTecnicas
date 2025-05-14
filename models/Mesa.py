from typing import List
from .Jugador import Jugador  # Asegúrate de tener esta clase en tu proyecto
from .Juego import Juego      # Clase base abstracta Juego

class Mesa:

    def __init__(self, mesa_id: str, juego: Juego, canJugadores: int, jugadores: List[Jugador] = None, activa: bool = True):
        self.mesa_id = mesa_id  # Cambié id a mesa_id
        self.juego = juego
        self.canJugadores = canJugadores  # Cantidad máxima de jugadores
        self.jugadores = jugadores if jugadores else []
        self.activa = activa

    def agregar_jugador(self, jugador: Jugador):
        """Agrega un jugador a la mesa."""
        if len(self.jugadores) >= self.canJugadores:
            raise ValueError(f"No se pueden agregar más jugadores. La mesa admite hasta {self.canJugadores} jugadores.")
        self.jugadores.append(jugador)

    def remover_jugador(self, jugador_id: str):
        """Remueve un jugador por su ID."""
        self.jugadores = [j for j in self.jugadores if j.jugador_id != jugador_id]

    def iniciar_juego(self):
        """Inicia el juego con los jugadores actuales."""
        if not self.activa:
            raise RuntimeError("La mesa está inactiva.")
        if len(self.jugadores) < 1:
            raise ValueError("No hay jugadores en la mesa.")
        if len(self.jugadores) > self.canJugadores:
            raise ValueError(f"La mesa solo admite {self.canJugadores} jugadores.")
        print(f"Iniciando el juego de {self.juego.get_nombre()} con {len(self.jugadores)} jugadores.")

