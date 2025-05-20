from collections import deque

class Jugador:
    def __init__(self, nombre: str, jugador_id: str, saldo: float, jugadas=None):
        self._nombre = nombre
        self._jugador_id = jugador_id
        self._saldo = saldo
        self._jugadas = deque(jugadas if jugadas else [], maxlen=10)

    # Getter y Setter para nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    # Getter y Setter para jugador_id
    @property
    def jugador_id(self):
        return self._jugador_id

    @jugador_id.setter
    def jugador_id(self, value):
        self._jugador_id = value

    # Getter y Setter para saldo
    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    # Getter y Setter para jugadas
    @property
    def jugadas(self):
        return list(self._jugadas)

    @jugadas.setter
    def jugadas(self, value):
        self._jugadas = deque(value, maxlen=10)

    # Método para agregar una jugada
    def agregar_jugada(self, jugada: str):
        self._jugadas.append(jugada)

    # Método para mostrar información del jugador
    def mostrarInfo(self):
        print(f"Nombre: {self.nombre}")
        print(f"ID: {self.jugador_id}")
        print(f"Saldo: {self.saldo}")
        print("Jugadas recientes:")
        for j in self.jugadas:
            print(f"- {j}")
