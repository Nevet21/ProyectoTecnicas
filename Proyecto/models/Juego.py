from abc import ABC, abstractmethod

class Juego(ABC):
    """Abstract base class representing a casino game"""
    
    def __init__(self, nombre, tipoJuego):
        """
        Initialize a game instance
        
        Args:
            nombre: Name of the game
            tipoJuego: Type/category of the game
        """
        self.nombre = nombre  # Game name
        self.tipoJuego = tipoJuego  # Game type/category

    # Getter for nombre
    def get_nombre(self):
        """Get the game name"""
        return self.nombre

    # Setter for nombre
    def set_nombre(self, nombre):
        """Set the game name"""
        self.nombre = nombre

    # Getter for tipoJuego
    def get_tipoJuego(self):
        """Get the game type/category"""
        return self.tipoJuego

    # Setter for tipoJuego
    def set_tipoJuego(self, tipoJuego):
        """Set the game type/category"""
        self.tipoJuego = tipoJuego