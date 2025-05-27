from abc import ABC, abstractmethod

class Juego(ABC):
    def __init__(self, nombre, tipoJuego):
        self.nombre = nombre
        self.tipoJuego = tipoJuego

    # Getter para nombre
    def get_nombre(self):
        return self.nombre

    # Setter para nombre
    def set_nombre(self, nombre):
        self.nombre = nombre

    # Getter para tipoJuego
    def get_tipoJuego(self):
        return self.tipoJuego

    # Setter para tipoJuego
    def set_tipoJuego(self, tipoJuego):
        self.tipoJuego = tipoJuego


