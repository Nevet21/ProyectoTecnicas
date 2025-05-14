import os
from models.Juego import Juego  # Asegúrate de que la clase Juego tenga atributos nombre y tipoJuego

class JuegoService:
    def __init__(self, archivo='juegos.txt'):
        self.juegos = []
        self.archivo = archivo
        self.proximo_id = 1
        self._cargar_juegos()

    def _cargar_juegos(self):
        self.juegos.clear()

        if not os.path.exists(self.archivo):
            open(self.archivo, 'w').close()
            return

        with open(self.archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(", ")
                if len(partes) == 3:
                    juego_id, nombre, tipoJuego = partes
                    juego = Juego(nombre, tipoJuego)
                    juego.juego_id = juego_id
                    self.juegos.append(juego)

        if self.juegos:
            ultimo_id = int(self.juegos[-1].juego_id[1:])
            self.proximo_id = ultimo_id + 1
        else:
            self.proximo_id = 1


    def _guardar_juegos(self):
        with open(self.archivo, 'w') as f:
            for juego in self.juegos:
                f.write(f"{juego.juego_id}, {juego.get_nombre()}, {juego.get_tipoJuego()}\n")


    def crearJuego(self, nombre: str, tipoJuego: str):
        juego_id = f"J{self.proximo_id}"
        nuevo_juego = Juego(nombre, tipoJuego)
        nuevo_juego.juego_id = juego_id
        self.juegos.append(nuevo_juego)
        self.proximo_id += 1
        self._guardar_juegos()
        print(f"Juego '{nombre}' creado con ID {juego_id}.")

    def borrarJuego(self, juego_id: str):
        for juego in self.juegos:
            if getattr(juego, 'juego_id', None) == juego_id:
                self.juegos.remove(juego)
                self._guardar_juegos()
                print(f"Juego '{juego_id}' eliminado.")
                return
        print(f"Juego con ID {juego_id} no encontrado.")

    def buscarJuego(self, juego_id: str):
        for juego in self.juegos:
            if getattr(juego, 'juego_id', None) == juego_id:
                print(f"Juego encontrado: ID: {juego.juego_id}, Nombre: {juego.get_nombre()}, Tipo: {juego.get_tipoJuego()}")
                return juego
        print(f"Juego con ID {juego_id} no encontrado.")
        return None

    def actualizarJuego(self, juego_id: str, nombre=None, tipoJuego=None):
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
