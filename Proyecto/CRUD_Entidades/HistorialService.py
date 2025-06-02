import os
import json
from Proyecto.models.Historial import Historial
from Proyecto.models.Mesa import Mesa

class HistorialService:
    """Service for managing game history records with JSON file persistence"""
    
    def __init__(self, archivo='historiales.txt'):
        """Initialize history service with data file"""
        self.historiales = []  # In-memory list of history records
        self.archivo = archivo  # Data file path
        self._cargar_historiales()  # Load existing records

    def _cargar_historiales(self):
        """Load history records from JSON file"""
        if not os.path.exists(self.archivo):
            open(self.archivo, 'w').close()  # Create file if it doesn't exist
            return

        with open(self.archivo, 'r') as file:
            for linea in file:
                try:
                    # Parse JSON data for each history record
                    datos = json.loads(linea.strip())
                    mesa_dummy = Mesa(datos['mesa_id'], None, 0)  # Create dummy table object
                    historial = Historial(mesa_dummy, datos['historial_id'])
                    
                    if 'resultado' in datos:
                        historial.set_resultado(datos['resultado'])
                    
                    self.historiales.append(historial)
                except json.JSONDecodeError:
                    continue  # Skip malformed JSON lines

    def _guardar_historiales(self):
        """Save all history records to JSON file"""
        with open(self.archivo, 'w') as file:
            for historial in self.historiales:
                datos = {
                    'mesa_id': historial.get_mesa().mesa_id,
                    'historial_id': historial.get_historial_id(),
                    'fecha': historial.get_fecha(),
                    'resultado': historial.get_resultado()
                }
                file.write(json.dumps(datos) + '\n')  # Write as JSON line

    def _generar_nuevo_id(self):
        """Generate sequential history ID (H1, H2, etc.)"""
        if not self.historiales:
            return "H1"
        ultimo = self.historiales[-1].get_historial_id()
        numero = int(ultimo[1:]) + 1
        return f"H{numero}"

    def crearHistorial(self, mesa: Mesa) -> Historial:
        """Create new history record for a game table"""
        historial_id = self._generar_nuevo_id()
        nuevo = Historial(mesa, historial_id)
        self.historiales.append(nuevo)
        self._guardar_historiales()
        print(f"Historial {historial_id} creado para mesa {mesa.mesa_id}.")
        return nuevo

    def borrarHistorial(self, historial_id: str) -> bool:
        """Delete history record by ID. Returns success status"""
        original = len(self.historiales)
        self.historiales = [h for h in self.historiales if h.get_historial_id() != historial_id]
        if len(self.historiales) < original:
            self._guardar_historiales()
            print(f"Historial {historial_id} eliminado.")
            return True
        print(f"Historial {historial_id} no encontrado.")
        return False

    def buscarHistorial(self, historial_id: str) -> Historial:
        """Find history record by ID. Returns Historial or None"""
        for historial in self.historiales:
            if historial.get_historial_id() == historial_id:
                return historial
        return None

    def actualizarHistorial(self, historial_id: str, resultado: dict = None) -> bool:
        """Update history record results. Returns success status"""
        historial = self.buscarHistorial(historial_id)
        if historial:
            if resultado:
                historial.set_resultado(resultado)
            self._guardar_historiales()
            return True
        return False

    def obtener_historial_por_jugador(self, jugador_id: str) -> list:
        """Get all history records for a specific player"""
        return [h for h in self.historiales 
               if h.get_resultado() and jugador_id in h.get_resultado().get('jugadores', {})]

    def obtener_historial_por_mesa(self, mesa_id: str) -> list:
        """Get all history records for a specific game table"""
        return [h for h in self.historiales if h.get_mesa().mesa_id == mesa_id]