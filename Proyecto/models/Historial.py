from datetime import datetime
from .Mesa import Mesa

class Historial:
    """Class representing a game history record with table information and results"""
    
    def __init__(self, mesa: Mesa, historial_id: str, resultado=None):
        """
        Initialize a history record
        
        Args:
            mesa: Table object associated with this history
            historial_id: Unique identifier for the history record
            resultado: Dictionary containing game results (optional)
        """
        self.__mesa = mesa  # Associated table
        self.__historial_id = historial_id  # Unique ID
        self.__resultado = resultado or {}  # Game results dictionary
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Creation timestamp

    # Getter and setter for mesa
    def get_mesa(self) -> Mesa:
        """Get the associated table object"""
        return self.__mesa

    def set_mesa(self, mesa: Mesa):
        """Set the associated table object"""
        self.__mesa = mesa

    # Getter and setter for historial_id
    def get_historial_id(self) -> str:
        """Get history record ID"""
        return self.__historial_id

    def set_historial_id(self, historial_id: str):
        """Set history record ID"""
        self.__historial_id = historial_id

    # Getter and setter for resultado
    def get_resultado(self) -> dict:
        """Get game results dictionary"""
        return self.__resultado

    def set_resultado(self, resultado: dict):
        """Set game results dictionary"""
        self.__resultado = resultado

    # Getter for fecha
    def get_fecha(self) -> str:
        """Get creation timestamp (read-only)"""
        return self.__fecha

    def mostrar_info(self):
        """Display complete history information in console"""
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