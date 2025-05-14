import os
from models.Jugador import Jugador

class JugadorService:
    def __init__(self, archivo="jugadores.txt"):
        self.archivo = archivo
        self.jugadores = []
        self._cargar_jugadores()
        print("Jugadores cargados:", [j.nombre for j in self.jugadores])

        # Crear archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                pass
        
        self._cargar_jugadores()

    def _cargar_jugadores(self):
        self.jugadores.clear()
        with open(self.archivo, "r") as f:
            for linea in f:
                partes = linea.strip().split(", ")
                if len(partes) == 4:
                    nombre, jugador_id, saldo_str, jugadas_str = partes
                elif len(partes) == 3:  # Jugadas vacías
                    nombre, jugador_id, saldo_str = partes
                    jugadas_str = ""
                else:
                    print(f"[!] Línea malformada ignorada: {linea}")
                    continue

                try:
                    saldo = float(saldo_str.strip().replace(",", ""))
                    jugadas = jugadas_str.split("|") if jugadas_str else []
                    self.jugadores.append(Jugador(nombre, jugador_id, saldo, jugadas))
                except ValueError:
                    print(f"[!] Error al convertir saldo: {saldo_str}")



    def _guardar_jugadores(self):
        with open(self.archivo, "w") as f:
            for jugador in self.jugadores:
                jugadas_str = "|".join(jugador.jugadas)
                if jugadas_str:
                    f.write(f"{jugador.nombre}, {jugador.jugador_id}, {jugador.saldo}, {jugadas_str}\n")
                else:
                    f.write(f"{jugador.nombre}, {jugador.jugador_id}, {jugador.saldo}\n")


    def _generar_nuevo_id(self):
        if not self.jugadores:
            return "J1"
        ultimo_id = self.jugadores[-1].jugador_id
        numero = int(ultimo_id[1:]) + 1
        return f"J{numero}"

    def crear_jugador(self, nombre, saldo):
        nuevo_id = self._generar_nuevo_id()
        nuevo_jugador = Jugador(nombre, nuevo_id, saldo, [])
        self.jugadores.append(nuevo_jugador)
        self._guardar_jugadores()
        print(f"Jugador {nombre} creado con ID {nuevo_id}")
        
        return 

    def borrar_jugador(self, nombre=None, jugador_id=None):
        original = len(self.jugadores)
        self.jugadores = [j for j in self.jugadores if not (j.jugador_id == jugador_id or j.nombre == nombre)]
        if len(self.jugadores) < original:
            self._guardar_jugadores()
            print("Jugador eliminado.")
        else:
            print("Jugador no encontrado.")

    def buscar_jugador(self, nombre=None, jugador_id=None):
        for jugador in self.jugadores:
            if jugador.jugador_id == jugador_id or jugador.nombre == nombre:
                jugador.mostrarInfo()
                return
        print("Jugador no encontrado.")
        


    def actualizar_jugador(self, nombre=None, jugador_id=None):
        for jugador in self.jugadores:
            if jugador.jugador_id == jugador_id or jugador.nombre == nombre:
                nuevo_nombre = input("Ingrese nuevo nombre: ")
                nuevo_saldo = float(input("Ingrese nuevo saldo: "))
                jugador.nombre = nuevo_nombre
                jugador.saldo = nuevo_saldo
                self._guardar_jugadores()
                print("Jugador actualizado.")
                return
        print("Jugador no encontrado.")
        
    def agregarJugadas(self, lista, jugador_id=None, nombre=None):
        for jugador in self.jugadores:
            if jugador.jugador_id == jugador_id or jugador.nombre == nombre:
                jugadas=jugador.jugadas
                for value in lista:
                    jugadas.append(value)
                jugador.jugadas=jugadas
                self._guardar_jugadores()
                print("Jugadas agregadas.")
                return
        print("Jugador no encontrado.")
        
        
