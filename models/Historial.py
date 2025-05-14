from .Mesa import Mesa

class Historial:
    def __init__(self, mesa: Mesa, historial_id):
        self.__mesa = mesa
        self.__historial_id = historial_id

    # Getter y setter para mesa
    def get_mesa(self) -> Mesa:
        return self.__mesa

    def set_mesa(self, mesa: Mesa):
        self.__mesa = mesa

    # Getter y setter para historial_id
    def get_historial_id(self):
        return self.__historial_id

    def set_historial_id(self, historial_id):
        self.__historial_id=historial_id
