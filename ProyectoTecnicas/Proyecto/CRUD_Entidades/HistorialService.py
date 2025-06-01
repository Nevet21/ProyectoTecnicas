import os
import json
from Proyecto.models.Historial import Historial
from Proyecto.models.Mesa import Mesa

class HistorialService:
    def __init__(self, archivo='historiales.txt'):
        self.historiales = []
        self.archivo = archivo
        self._cargar_historiales()

    def _cargar_historiales(self):
        if not os.path.exists(self.archivo):
            open(self.archivo, 'w').close()
            return

        with open(self.archivo, 'r') as file:
            for linea in file:
                try:
                    datos = json.loads(linea.strip())
                    mesa_dummy = Mesa(datos['mesa_id'], None, 0)
                    historial = Historial(mesa_dummy, datos['historial_id'])
                    if 'resultado' in datos:
                        historial.set_resultado(datos['resultado'])
                    self.historiales.append(historial)
                except json.JSONDecodeError:
                    continue

    def _guardar_historiales(self):
        with open(self.archivo, 'w') as file:
            for historial in self.historiales:
                datos = {
                    'mesa_id': historial.get_mesa().mesa_id,
                    'historial_id': historial.get_historial_id(),
                    'fecha': historial.get_fecha(),
                    'resultado': historial.get_resultado()
                }
                file.write(json.dumps(datos) + '\n')

    def _generar_nuevo_id(self):
        if not self.historiales:
            return "H1"
        ultimo = self.historiales[-1].get_historial_id()
        numero = int(ultimo[1:]) + 1
        return f"H{numero}"

    def crearHistorial(self, mesa: Mesa) -> Historial:
        historial_id = self._generar_nuevo_id()
        nuevo = Historial(mesa, historial_id)
        self.historiales.append(nuevo)
        self._guardar_historiales()
        print(f"Historial {historial_id} creado para mesa {mesa.mesa_id}.")
        return nuevo

    def borrarHistorial(self, historial_id: str) -> bool:
        original = len(self.historiales)
        self.historiales = [h for h in self.historiales if h.get_historial_id() != historial_id]
        if len(self.historiales) < original:
            self._guardar_historiales()
            print(f"Historial {historial_id} eliminado.")
            return True
        print(f"Historial {historial_id} no encontrado.")
        return False

    def buscarHistorial(self, historial_id: str) -> Historial:
        for historial in self.historiales:
            if historial.get_historial_id() == historial_id:
                return historial
        return None

    def actualizarHistorial(self, historial_id: str, resultado: dict = None) -> bool:
        historial = self.buscarHistorial(historial_id)
        if historial:
            if resultado:
                historial.set_resultado(resultado)
            self._guardar_historiales()
            return True
        return False

    def obtener_historial_por_jugador(self, jugador_id: str) -> list:
        return [h for h in self.historiales 
               if h.get_resultado() and jugador_id in h.get_resultado().get('jugadores', {})]

    def obtener_historial_por_mesa(self, mesa_id: str) -> list:
        return [h for h in self.historiales if h.get_mesa().mesa_id == mesa_id]