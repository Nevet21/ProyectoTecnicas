from collections import deque
from typing import List, Dict, Any

class Jugador:
    """Class representing a casino player with game history and statistics"""
    
    def __init__(self, nombre: str, jugador_id: str, saldo: float, apuesta: float, jugadas=None, historial=None):
        """
        Initialize a player instance
        
        Args:
            nombre: Player name
            jugador_id: Unique player identifier
            saldo: Current balance
            apuesta: Current bet amount
            jugadas: Recent moves (optional)
            historial: Game history (optional)
        """
        self._nombre = nombre  # Player name
        self._jugador_id = jugador_id  # Unique ID
        self._saldo = saldo  # Current balance
        self._jugadas = deque(jugadas if jugadas else [], maxlen=10)  # Last 10 moves
        self._apuesta = apuesta  # Current bet amount
        self._historial = historial if historial else []  # Game history
        self.juegos_ganados = 0  # Games won counter
        self.juegos_perdidos = 0  # Games lost counter

    @property
    def historial(self) -> List[Dict[str, Any]]:
        """Get player's game history (list of event dictionaries)"""
        return self._historial
    
    @historial.setter
    def historial(self, value: List[Dict[str, Any]]):
        """Set player's game history"""
        self._historial = value
        
    def agregar_historial(self, evento: Dict[str, Any]):
        """Add a game event to player's history (Spanish method name preserved)"""
        self._historial.append(evento)
        
    @property
    def apuesta(self) -> float:
        """Get current bet amount (returns float)"""
        return self._apuesta

    @apuesta.setter
    def apuesta(self, valor: float) -> None:
        """
        Set new bet amount with validation
        
        Args:
            valor: New bet amount (must be non-negative number)
            
        Raises:
            TypeError: If value cannot be converted to float
            ValueError: If value is negative
        """
        try:
            valor = float(valor)  # Convert to float
        except (TypeError, ValueError):
            raise TypeError("La apuesta debe ser un número (float o int).")
        
        if valor < 0:
            raise ValueError("La apuesta no puede ser negativa.")
        self._apuesta = valor

    @property
    def nombre(self):
        """Get player name"""
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        """Set player name"""
        self._nombre = value

    @property
    def jugador_id(self):
        """Get player ID"""
        return self._jugador_id

    @jugador_id.setter
    def jugador_id(self, value):
        """Set player ID"""
        self._jugador_id = value

    @property
    def saldo(self):
        """Get current balance"""
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        """Set current balance"""
        self._saldo = value

    @property
    def jugadas(self):
        """Get recent moves (as list)"""
        return list(self._jugadas)

    @jugadas.setter
    def jugadas(self, value):
        """Set recent moves (converts to deque with maxlen=10)"""
        self._jugadas = deque(value, maxlen=10)

    def agregar_jugada(self, jugada: str):
        """Add a move to recent moves (Spanish method name preserved)"""
        self._jugadas.append(jugada)

    def mostrarInfo(self):
        """Display player information (Spanish method name preserved)"""
        print(f"Nombre: {self.nombre}")
        print(f"ID: {self.jugador_id}")
        print(f"Saldo: {self.saldo}")
        print("Jugadas recientes:")
        for j in self.jugadas:
            print(f"- {j}")