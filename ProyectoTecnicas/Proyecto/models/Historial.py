from datetime import datetime
from .Mesa import Mesa

class Historial:
    def __init__(self, mesa: Mesa, historial_id: str, resultado=None):
        self.__mesa = mesa
        self.__historial_id = historial_id
        self.__resultado = resultado or {}
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Getter y setter para mesa
    def get_mesa(self) -> Mesa:
        return self.__mesa

    def set_mesa(self, mesa: Mesa):
        self.__mesa = mesa

    # Getter y setter para historial_id
    def get_historial_id(self) -> str:
        return self.__historial_id

    def set_historial_id(self, historial_id: str):
        self.__historial_id = historial_id

    # Getter y setter para resultado
    def get_resultado(self) -> dict:
        return self.__resultado

    def set_resultado(self, resultado: dict):
        self.__resultado = resultado

    # Getter para fecha
    def get_fecha(self) -> str:
        return self.__fecha

    def mostrar_info(self):
        """Muestra la información completa del historial"""
        print(f"\nHistorial ID: {self.__historial_id}")
        print(f"Fecha: {self.__fecha}")
        print(f"Mesa ID: {self.__mesa.mesa_id}")
        if self.__resultado:
            print("\nResultados:")
            print(f"Juego: {self.__resultado.get('juego', 'N/A')}")
            print(f"Ganador: {self.__resultado.get('nombre_ganador', 'N/A')}")
            
            if 'jugadores' in self.__resultado:
                print("\nDetalle por jugador:")
                for jugador_id, datos in self.__resultado['jugadores'].items():
                    resultado = datos.get('resultado', 'N/A')
                    ganancia = datos.get('ganancia', 0)
                    print(f"- {datos['nombre']}: {resultado} (Ganancia: ${ganancia})")
