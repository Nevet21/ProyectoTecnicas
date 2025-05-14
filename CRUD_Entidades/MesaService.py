import os
from models.Mesa import Mesa
from models.Juego import Juego

class MesaService:
    def __init__(self, archivo="mesas.txt"):
        self.archivo = archivo
        self.mesas = []

        # Crear el archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                pass

        self._cargar_mesas()

    def _cargar_mesas(self):
        self.mesas.clear()
        with open(self.archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split(", ")

                if len(partes) != 4:
                    print(f"[!] Línea malformada ignorada: {linea}")
                    continue

                mesa_id, nombre_juego, can_jugadores_str, activa_str = partes

                try:
                    can_jugadores = int(can_jugadores_str.strip().replace(",", ""))
                    activa = activa_str.strip() == "True"
                    juego = Juego(nombre_juego.strip(), "Desconocido")
                    mesa = Mesa(mesa_id.strip(), juego, can_jugadores, [], activa)
                    self.mesas.append(mesa)
                except ValueError:
                    print(f"[!] Error al cargar mesa: {linea}")


    def _guardar_mesas(self):   
        with open(self.archivo, "w") as f:
            for mesa in self.mesas:
                linea = f"{mesa.mesa_id}, {mesa.juego.get_nombre()}, {mesa.canJugadores}, {mesa.activa}"
                f.write(linea + "\n")

    def _generar_nuevo_id(self):
        if not self.mesas:
            return "M1"
        ultimo_id = self.mesas[-1].mesa_id
        numero = int(ultimo_id[1:]) + 1
        return f"M{numero}"

    def crearMesa(self, juego: Juego, canJugadores: int, jugadores=None, activa=True):
        mesa_id = self._generar_nuevo_id()
        nueva_mesa = Mesa(mesa_id, juego, canJugadores, jugadores, activa)
        self.mesas.append(nueva_mesa)
        self._guardar_mesas()
        print(f"Mesa {mesa_id} creada con éxito.")

    def borrarMesa(self, mesa_id: str):
        original = len(self.mesas)
        self.mesas = [mesa for mesa in self.mesas if mesa.mesa_id != mesa_id]
        if len(self.mesas) < original:
            self._guardar_mesas()
            print(f"Mesa {mesa_id} eliminada.")
        else:
            print(f"Mesa {mesa_id} no encontrada.")

    def buscarMesa(self, mesa_id: str):
        for mesa in self.mesas:
            if mesa.mesa_id == mesa_id:
                print(f"Mesa encontrada: ID: {mesa.mesa_id}, Juego: {mesa.juego.get_nombre()}, Jugadores: {len(mesa.jugadores)}, Activa: {mesa.activa}")
                return
        print(f"Mesa con ID {mesa_id} no encontrada.")

    def actualizarMesa(self, mesa_id: str, nombre_juego=None, canJugadores=None, activa=None):
        for mesa in self.mesas:
            if mesa.mesa_id == mesa_id:
                if nombre_juego:
                    mesa.juego.set_nombre(nombre_juego)
                if canJugadores:
                    mesa.canJugadores = canJugadores
                if activa is not None:
                    mesa.activa = activa
                self._guardar_mesas()
                print(f"Mesa {mesa_id} actualizada.")
                return
        print(f"Mesa con ID {mesa_id} no encontrada.")

