from typing import List, Deque
from collections import deque
from .Jugador import Jugador
from .Juego import Juego

class Mesa:
    def __init__(self, mesa_id: str, juego: Juego, canJugadores: int, 
                 jugadores: List[Jugador] = None, activa: bool = True):
        self.mesa_id = mesa_id
        self.juego = juego
        self.canJugadores = canJugadores
        self.jugadores = jugadores if jugadores else []
        self.cola_espera: Deque[Jugador] = deque()  # Cola para jugadores en espera
        self.activa = activa

    def agregar_jugador(self, jugador: Jugador):
        """Agrega un jugador a la mesa o a la cola de espera si está llena."""
        if len(self.jugadores) < self.canJugadores:
            self.jugadores.append(jugador)
            return True  # Jugador agregado directamente
        else:
            self.cola_espera.append(jugador)
            return False  # Jugador puesto en cola de espera

    def remover_jugador(self, jugador_id: str):
        """Remueve un jugador por su ID y mueve el siguiente de la cola si hay espacio."""
        # Eliminar jugador actual
        jugadores_originales = len(self.jugadores)
        self.jugadores = [j for j in self.jugadores if j.jugador_id != jugador_id]
        
        # Si se eliminó un jugador y hay gente en cola, mover siguiente jugador
        if len(self.jugadores) < jugadores_originales and self.cola_espera:
            siguiente_jugador = self.cola_espera.popleft()
            self.jugadores.append(siguiente_jugador)
            return siguiente_jugador  # Devuelve el jugador que entró
        return None

    def obtener_cola_espera(self) -> List[Jugador]:
        """Devuelve una lista de jugadores en espera."""
        return list(self.cola_espera)

    def iniciar_juego(self):
        """Inicia el juego con los jugadores actuales."""
        if not self.activa:
            raise RuntimeError("La mesa está inactiva.")
        if len(self.jugadores) < 1:
            raise ValueError("No hay jugadores en la mesa.")
        if len(self.jugadores) > self.canJugadores:
            raise ValueError(f"La mesa solo admite {self.canJugadores} jugadores.")
        print(f"Iniciando el juego de {self.juego.get_nombre()} con {len(self.jugadores)} jugadores.")
        print(f"Jugadores en espera: {len(self.cola_espera)}")