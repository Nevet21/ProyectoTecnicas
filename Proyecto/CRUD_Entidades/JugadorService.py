import os
from collections import deque
from Proyecto.models.Jugador import Jugador

class JugadorService:
    """Service for managing players with file persistence"""
    
    def __init__(self, archivo="jugadores.txt"):
        """Initialize with data file path. Creates file if nonexistent"""
        self.archivo = archivo
        self.jugadores = []
        
        # Create file if it doesn't exist
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                pass
        
        self._cargar_jugadores()
        print("Jugadores cargados:", [j.nombre for j in self.jugadores])

    def _cargar_jugadores(self):
        """Load players from data file into memory"""
        self.jugadores.clear()
        with open(self.archivo, "r") as f:
            for linea in f:
                partes = [p.strip() for p in linea.strip().split(", ")]
                
                # Handle different file formats
                if len(partes) == 5:
                    nombre, jugador_id, saldo_str, apuesta_str, jugadas_str = partes
                elif len(partes) == 4:
                    nombre, jugador_id, saldo_str, apuesta_str = partes
                    jugadas_str = ""
                else:
                    print(f"[!] Línea malformada ignorada: {linea}")
                    continue

                try:
                    saldo = float(saldo_str)
                    apuesta = float(apuesta_str)
                    jugadas = jugadas_str.split("|") if jugadas_str else []
                    self.jugadores.append(Jugador(nombre, jugador_id, saldo, apuesta, jugadas))
                except ValueError as e:
                    print(f"[!] Error al procesar línea: {linea}. Error: {e}")

    def _guardar_jugadores(self):
        """Save all players to data file"""
        with open(self.archivo, "w") as f:
            for jugador in self.jugadores:
                jugadas_str = "|".join(jugador.jugadas)
                linea = f"{jugador.nombre}, {jugador.jugador_id}, {jugador.saldo}, {jugador.apuesta}"
                if jugadas_str:
                    linea += f", {jugadas_str}"
                f.write(linea + "\n")

    def _generar_nuevo_id(self):
        """Generate sequential player ID (J1, J2, etc.)"""
        if not self.jugadores:
            return "J1"
        ids_numericos = [int(j.jugador_id[1:]) for j in self.jugadores if j.jugador_id.startswith("J")]
        nuevo_numero = max(ids_numericos) + 1 if ids_numericos else 1
        return f"J{nuevo_numero}"

    def crear_jugador(self, nombre: str, saldo_inicial: float = 0.0, apuesta_inicial: float = 0.0):
        """Create new player with auto-generated ID"""
        nuevo_id = self._generar_nuevo_id()
        nuevo_jugador = Jugador(nombre, nuevo_id, saldo_inicial, apuesta_inicial, [])
        self.jugadores.append(nuevo_jugador)
        self._guardar_jugadores()
        print(f"Jugador {nombre} creado con ID {nuevo_id}")
        return nuevo_jugador

    def borrar_jugador(self, nombre=None, jugador_id=None):
        """Delete player by name or ID. Returns success status"""
        original_count = len(self.jugadores)
        self.jugadores = [j for j in self.jugadores 
        if not (j.jugador_id == jugador_id or j.nombre == nombre)]
        
        if len(self.jugadores) < original_count:
            self._guardar_jugadores()
            print("Jugador eliminado.")
            return True
        else:
            print("Jugador no encontrado.")
            return False

    def buscar_jugador(self, nombre=None, jugador_id=None):
        """Find player by name or ID. Returns Jugador or None"""
        for jugador in self.jugadores:
            if (jugador_id and jugador.jugador_id == jugador_id) or \
            (nombre and jugador.nombre == nombre):
                return jugador
        print("Jugador no encontrado.")
        return None

    def actualizar_jugador(self, jugador_id=None, nombre=None, 
        nuevo_nombre=None, nuevo_saldo=None, nueva_apuesta=None):
        """Update player properties. Returns success status"""
        jugador = self.buscar_jugador(nombre=nombre, jugador_id=jugador_id)
        if not jugador:
            return False
            
        if nuevo_nombre:
            jugador.nombre = nuevo_nombre
        if nuevo_saldo is not None:
            jugador.saldo = nuevo_saldo
        if nueva_apuesta is not None:
            jugador.apuesta = nueva_apuesta
            
        self._guardar_jugadores()
        print("Jugador actualizado.")
        return True

    def actualizar_saldo(self, jugador_id, cambio: float):
        """Update player's balance directly. Returns success status"""
        jugador = self.buscar_jugador(jugador_id=jugador_id)
        if not jugador:
            return False
            
        jugador.saldo = cambio
        self._guardar_jugadores()
        return True

    def actualizar_apuesta(self, jugador_id, nueva_apuesta: float):
        """Update player's bet amount. Returns success status"""
        jugador = self.buscar_jugador(jugador_id=jugador_id)
        if not jugador:
            return False
            
        jugador.apuesta = nueva_apuesta
        self._guardar_jugadores()
        return True
        
    def agregar_jugadas(self, jugadas: list, jugador_id=None, nombre=None):
        """Add game history to player. Returns success status"""
        jugador = self.buscar_jugador(nombre=nombre, jugador_id=jugador_id)
        if not jugador:
            return False
            
        for jugada in jugadas:
            jugador.agregar_jugada(jugada)
            
        self._guardar_jugadores()
        print(f"Jugadas agregadas a {jugador.nombre}: {jugadas}")
        return True
    
    def obtener_jugadores(self):
        """Get copy of all players list"""
        return self.jugadores.copy()

    def obtener_ranking(self):
        """Get players ranked by balance (highest first)"""
        return sorted(self.jugadores, key=lambda j: j.saldo, reverse=True)