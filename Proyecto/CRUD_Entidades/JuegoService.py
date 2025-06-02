import os
from Proyecto.models.Juego import Juego  # Ensure Juego class has nombre and tipoJuego attributes

class JuegoService:
    """Service for managing casino games with file persistence"""
    
    def __init__(self, archivo='juegos.txt'):
        """Initialize game service with data file"""
        self.juegos = []  # In-memory game list
        self.archivo = archivo  # Data file path
        self.proximo_id = 1  # Next available game ID
        self._cargar_juegos()  # Load existing games

    def _cargar_juegos(self):
        """Load games from data file into memory"""
        self.juegos.clear()

        # Create file if it doesn't exist
        if not os.path.exists(self.archivo):
            open(self.archivo, 'w').close()
            return

        # Read and parse game data
        with open(self.archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(", ")
                if len(partes) == 3:  # Validate data format
                    juego_id, nombre, tipoJuego = partes
                    juego = Juego(nombre, tipoJuego)
                    juego.juego_id = juego_id
                    self.juegos.append(juego)

        # Set next available ID
        if self.juegos:
            ultimo_id = int(self.juegos[-1].juego_id[1:])
            self.proximo_id = ultimo_id + 1
        else:
            self.proximo_id = 1

    def _guardar_juegos(self):
        """Save all games to data file"""
        with open(self.archivo, 'w') as f:
            for juego in self.juegos:
                f.write(f"{juego.juego_id}, {juego.get_nombre()}, {juego.get_tipoJuego()}\n")

    def crearJuego(self, nombre: str, tipoJuego: str):
        """Create new game with auto-generated ID"""
        juego_id = f"J{self.proximo_id}"
        nuevo_juego = Juego(nombre, tipoJuego)
        nuevo_juego.juego_id = juego_id
        self.juegos.append(nuevo_juego)
        self.proximo_id += 1
        self._guardar_juegos()
        print(f"Juego '{nombre}' creado con ID {juego_id}.")

    def borrarJuego(self, juego_id: str):
        """Delete game by ID"""
        for juego in self.juegos:
            if getattr(juego, 'juego_id', None) == juego_id:
                self.juegos.remove(juego)
                self._guardar_juegos()
                print(f"Juego '{juego_id}' eliminado.")
                return
        print(f"Juego con ID {juego_id} no encontrado.")

    def buscarJuego(self, juego_id: str):
        """Find game by ID. Returns Juego object or None"""
        for juego in self.juegos:
            if getattr(juego, 'juego_id', None) == juego_id:
                print(f"Juego encontrado: ID: {juego.juego_id}, Nombre: {juego.get_nombre()}, Tipo: {juego.get_tipoJuego()}")
                return juego
        print(f"Juego con ID {juego_id} no encontrado.")
        return None

    def actualizarJuego(self, juego_id: str, nombre=None, tipoJuego=None):
        """Update game properties"""
        for juego in self.juegos:
            if getattr(juego, 'juego_id', None) == juego_id:
                if nombre:
                    juego.set_nombre(nombre)
                if tipoJuego:
                    juego.set_tipoJuego(tipoJuego)
                self._guardar_juegos()
                print(f"Juego '{juego_id}' actualizado.")
                return
        print(f"Juego con ID {juego_id} no encontrado.")