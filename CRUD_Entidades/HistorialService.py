import os
from models.Historial import Historial
from models.Mesa import Mesa

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
                datos = linea.strip().split(',')
                if len(datos) >= 2:
                    mesa_id = datos[0]
                    historial_id = datos[1]
                    mesa_dummy = Mesa(mesa_id, None, 0)  # Juego y jugadores se setean como None o vacío
                    historial = Historial(mesa_dummy, historial_id)
                    self.historiales.append(historial)

    def _guardar_historiales(self):
        with open(self.archivo, 'w') as file:
            for historial in self.historiales:
                file.write(f"{historial.get_mesa().mesa_id},{historial.get_historial_id()}\n")

    def _generar_nuevo_id(self):
        if not self.historiales:
            return "H1"
        ultimo = self.historiales[-1].get_historial_id()
        numero = int(ultimo[1:]) + 1
        return f"H{numero}"

    def crearHistorial(self, mesa: Mesa):
        historial_id = self._generar_nuevo_id()
        nuevo = Historial(mesa, historial_id)
        self.historiales.append(nuevo)
        self._guardar_historiales()
        print(f"Historial {historial_id} creado para mesa {mesa.mesa_id}.")

    def borrarHistorial(self, historial_id):
        original = len(self.historiales)
        self.historiales = [h for h in self.historiales if h.get_historial_id() != historial_id]
        if len(self.historiales) < original:
            self._guardar_historiales()
            print(f"Historial {historial_id} eliminado.")
        else:
            print(f"Historial {historial_id} no encontrado.")

    def buscarHistorial(self, historial_id):
        for historial in self.historiales:
            if historial.get_historial_id() == historial_id:
                print(f"Historial encontrado: ID: {historial_id}, Mesa: {historial.get_mesa().mesa_id}")
                return
        print(f"Historial con ID {historial_id} no encontrado.")

    def actualizarHistorial(self, historial_id, nueva_mesa: Mesa = None):
        for historial in self.historiales:
            if historial.get_historial_id() == historial_id:
                if nueva_mesa:
                    historial.set_mesa(nueva_mesa)
                self._guardar_historiales()
                print(f"Historial {historial_id} actualizado.")
                return
        print(f"Historial con ID {historial_id} no encontrado.")
