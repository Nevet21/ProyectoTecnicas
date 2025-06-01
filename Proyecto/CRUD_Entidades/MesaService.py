from typing import List
import os
from Proyecto.models.Mesa import Mesa
from Proyecto.models.Juego import Juego
from Proyecto.models.Jugador import Jugador

class MesaService:
    def __init__(self, archivo="mesas.txt"):
        self.archivo = archivo
        self.mesas = []
        
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                pass
        
        self._cargar_mesas()

    def _cargar_mesas(self):
        self.mesas.clear()
        with open(self.archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split("; ")
                
                if len(partes) < 4:
                    print(f"[!] Línea malformada ignorada: {linea}")
                    continue

                try:
                    mesa_id = partes[0].strip()
                    nombre_juego = partes[1].strip()
                    can_jugadores = int(partes[2].strip())
                    activa = partes[3].strip() == "True"
                    
                    jugadores_ids = []
                    if len(partes) > 4 and partes[4].strip():
                        jugadores_ids = [id.strip() for id in partes[4].split(",")]
                    
                    juego = Juego(nombre_juego, "Mesa")
                    mesa = Mesa(mesa_id, juego, can_jugadores, [], activa)
                    mesa._jugadores_ids = jugadores_ids
                    self.mesas.append(mesa)
                except ValueError as e:
                    print(f"[!] Error al cargar mesa: {linea}. Error: {e}")

    def _guardar_mesas(self):
        with open(self.archivo, "w") as f:
            for mesa in self.mesas:
                jugadores_ids = [jugador.jugador_id for jugador in mesa.jugadores]
                jugadores_str = ", ".join(jugadores_ids) if jugadores_ids else ""
                
                linea = (
                    f"{mesa.mesa_id}; {mesa.juego.get_nombre()}; "
                    f"{mesa.canJugadores}; {mesa.activa}; {jugadores_str}"
                )
                f.write(linea + "\n")

    def _generar_nuevo_id(self):
        if not self.mesas:
            return "M1"
        ultimo_id = self.mesas[-1].mesa_id
        numero = int(ultimo_id[1:]) + 1
        return f"M{numero}"

    def crearMesa(self, juego: Juego, canJugadores: int, jugadores=None, activa=True):
        # Verificar límites para Dado Mentiroso
        if hasattr(juego, 'min_jugadores') and hasattr(juego, 'max_jugadores'):
            if canJugadores < juego.min_jugadores or canJugadores > juego.max_jugadores:
                print(f"Error: Este juego requiere entre {juego.min_jugadores} y {juego.max_jugadores} jugadores")
                return None
        
        mesa_id = self._generar_nuevo_id()
        nueva_mesa = Mesa(mesa_id, juego, canJugadores, jugadores or [], activa)
        self.mesas.append(nueva_mesa)
        self._guardar_mesas()
        return nueva_mesa

    def borrarMesa(self, mesa_id: str):
        original = len(self.mesas)
        self.mesas = [mesa for mesa in self.mesas if mesa.mesa_id != mesa_id]
        if len(self.mesas) < original:
            self._guardar_mesas()
            return True
        return False

    def buscarMesa(self, mesa_id: str):
        for mesa in self.mesas:
            if mesa.mesa_id == mesa_id:
                return mesa
        return None

    def actualizarMesa(self, mesa_id: str, nombre_juego=None, canJugadores=None, activa=None):
        mesa = self.buscarMesa(mesa_id)
        if mesa:
            if nombre_juego:
                mesa.juego.set_nombre(nombre_juego)
            if canJugadores is not None:
                mesa.canJugadores = canJugadores
            if activa is not None:
                mesa.activa = activa
            self._guardar_mesas()
            return True
        return False

    def agregar_jugador_a_mesa(self, mesa_id: str, jugador: Jugador):
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False, "Mesa no encontrada"
        
        resultado = mesa.agregar_jugador(jugador)
        self._guardar_mesas()
        
        if resultado:
            return True, f"{jugador.nombre} se unió a la mesa {mesa_id}"
        else:
            return True, f"{jugador.nombre} fue agregado a la cola de espera de la mesa {mesa_id}"

    def mover_siguiente_jugador(self, mesa_id: str):
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False, "Mesa no encontrada"
        
        if len(mesa.jugadores) >= mesa.canJugadores:
            return False, "La mesa está llena"
        
        if not mesa.cola_espera:
            return False, "No hay jugadores en la cola de espera"
        
        jugador = mesa.cola_espera.popleft()
        mesa.jugadores.append(jugador)
        self._guardar_mesas()
        return True, f"{jugador.nombre} ha sido movido a la mesa {mesa_id}"

    def obtener_cola_espera(self, mesa_id: str):
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa.obtener_cola_espera()

    def cargar_jugadores_en_mesas(self, jugador_service):
        for mesa in self.mesas:
            if hasattr(mesa, '_jugadores_ids'):
                for jugador_id in mesa._jugadores_ids:
                    jugador = jugador_service.buscar_jugador(jugador_id=jugador_id)
                    if jugador:
                        mesa.agregar_jugador(jugador)
                if hasattr(mesa, '_jugadores_ids'):
                    delattr(mesa, '_jugadores_ids')