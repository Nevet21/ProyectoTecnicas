from Proyecto.models.Juego import Juego
import random
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.models.Jugador import Jugador

class BlackJack(Juego):
    def __init__(self, nombre, tipoJuego, jugadores):
        super().__init__(nombre, tipoJuego)
        self.jugadores = jugadores
        self.baraja = []
        self.cartasJugadores = []
        self.crupier = []
        self.serviceJugador = JugadorService()
        self.apuestas = {}  # Diccionario para guardar las apuestas
    
    def apuesta(self):
        """Maneja las apuestas iniciales de los jugadores"""
        for jugador in self.jugadores:
                print(f"{jugador.nombre} su saldo es de: {jugador.saldo}")
                while True:
                    try:
                        apuesta = float(input(f"Ingrese su apuesta (máx {jugador.saldo}): "))
                        if apuesta <= 0 or apuesta > jugador.saldo:
                            print("Apuesta inválida. Intente nuevamente.")
                            continue
                        
                        # Guardar la apuesta y restar del saldo
                        self.apuestas[jugador.jugador_id] = apuesta
                        jugador.saldo -= apuesta
                        jugador.apuesta = apuesta
                        break
                    except ValueError:
                        print("Debe ingresar un número válido.")
    
    def crear_Mazo(self, baraja=None, aux=0, cartas=None, contador=0):
        if baraja is None:
            baraja = []
        if cartas is None:
            cartas = [2, 3, 4, 5, 6, 7, 8, 9,10, "J", "Q", "K", "A"]
        
        palos = ['♠', '♥', '♦', '♣']
        
        if len(baraja) == 52:
            print("Terminó de barajar")
            self.baraja = baraja  # Guardamos la baraja en el atributo de la clase
            return baraja
        
        # Añadir carta actual (valor + palo)
        baraja.append(f"{cartas[contador]}{palos[aux]}")
        
        if contador == 12:  # Cambiamos a 11 porque los índices van de 0 a 11
            contador = 0
            aux += 1
        else:
            contador += 1
        
        return self.crear_Mazo(baraja, aux, cartas, contador)
    
    def barajar(self):
        """Baraja aleatoriamente la baraja"""
        random.shuffle(self.baraja)  # Esto mezcla la lista in-place
        print("Baraja mezclada aleatoriamente")
        return self.baraja
    
    def repartirCarta(self,cartasJugador,canCartas):
        if len(cartasJugador)==canCartas:
            return cartasJugador
        else:
            cartasJugador.append(self.baraja.pop(0))
            return self.repartirCarta(cartasJugador,canCartas)
        
    def repartirCartas(self):
        for jugador in self.jugadores:
            cartas=self.repartirCarta([],2)
            self.cartasJugadores.append((jugador, cartas))  # Guarda como tupla
        self.crupier=self.repartirCarta([],2)
        print("CARTA CRUPIER: ")
        print(self.crupier[0])
        return self.cartasJugadores
    
    def seguirJugando(self):
        for i in range(len(self.jugadores)):
            jugador, cartas = self.cartasJugadores[i]  # Obtenemos jugador y sus cartas
            
            while True:
                # Calculamos la suma actualizada en cada turno
                suma = self.calcular_suma_cartas(cartas)
                
                # Verificamos si el jugador ya perdió
                if suma > 21:
                    self.serviceJugador.agregar_jugadas(
                        ("Perdió",str(jugador.apuesta)),jugador.jugador_id  # Eliminé str(saldo) porque no está definido
                    )
                    self.serviceJugador.actualizar_saldo(jugador.jugador_id,((jugador.saldo-jugador.apuesta)))
                    print(f"Jugador {self.jugadores[i].nombre} sale de la mesa (Se pasó de 21)")
                    break
               
                
                # Preguntamos por la acción del jugador
                opcion = input(f"{jugador.nombre}, ¿Quieres PEDIR (1) o PLANTARTE (2)? ").strip()
                
                if opcion == "1":
                    nueva_carta = self.repartirCarta([],1)  # Repartimos 1 carta
                    cartas.extend(nueva_carta)  # Agregamos a su mano
                    print(f"{jugador.nombre} recibe: {nueva_carta}. Cartas: {cartas} | Suma: {self.calcular_suma_cartas(cartas)}")
                    
                elif opcion == "2":
                    print(f"{jugador.nombre} se planta con: {cartas} | Suma: {suma}")
                    break
                    
                else:
                    print("Opción inválida. Ingresa 1 o 2.")
                
                
    def calcular_suma_cartas(self,cartas):
        suma = 0
        ases = 0
        
        for carta in cartas:
            valor = carta[:-1]  # Elimina el palo (asume formato "valor+palo" como "A♠", "10♦")
            
            if valor in ['J', 'Q', 'K']:
                suma += 10
            elif valor == 'A':
                suma += 11
                ases += 1
            else:
                suma += int(valor)
        
        # Ajustar Ases si la suma > 21
        while suma > 21 and ases > 0:
            suma -= 10
            ases -= 1
        
        return suma


                    
    def calcular_resultados(self):
            """Calcula los resultados finales y actualiza saldos"""
            suma_crupier = self.calcular_suma_cartas(self.crupier)
            resultados = []
            
            for jugador, cartas in self.cartasJugadores:
                suma_jugador = self.calcular_suma_cartas(cartas)
                apuesta = self.apuestas[jugador.jugador_id]
                
                if suma_jugador > 21:  # Jugador pierde
                    resultado = "PERDIO"
                    ganancia = -apuesta
                    jugador.juegos_perdidos += 1
                elif suma_crupier > 21 or suma_jugador > suma_crupier:  # Jugador gana
                    resultado = "GANO"
                    ganancia = apuesta * 2  # Gana el doble (apuesta + ganancia)
                    jugador.saldo += ganancia
                    jugador.juegos_ganados += 1
                elif suma_jugador < suma_crupier:  # Jugador pierde
                    resultado = "PERDIO"
                    ganancia = -apuesta
                    jugador.juegos_perdidos += 1
                else:  # Empate
                    resultado = "EMPATO"
                    ganancia = 0
                    jugador.saldo += apuesta  # Devuelve la apuesta
                
                resultados.append({
                    'jugador': jugador,
                    'resultado': resultado,
                    'ganancia': ganancia,
                    'suma_jugador': suma_jugador,
                    'suma_crupier': suma_crupier
                })
                
                # Registrar jugada
                jugador.agregar_jugada(f"BlackJack|{resultado}|{ganancia}")
            
            return resultados

    def turnoCrupiert(self):
        suma = self.calcular_suma_cartas(self.crupier)
        while suma <= 16:
            cartaNueva = self.repartirCarta([], 1)
            self.crupier.extend(cartaNueva)
            suma = self.calcular_suma_cartas(self.crupier)
        
        return self.calcular_resultados()
                
            
    def gameOver(self,sumaC):
        for i in range(len(self.cartasJugadores)):
            jugador,cartas= self.cartasJugadores[i]
            sumaJugador=self.calcular_suma_cartas(cartas)
            if sumaJugador<sumaC:
                self.serviceJugador.agregar_jugadas(("PERDIO",str(jugador.apuesta)),jugador.jugador_id)
                print(jugador.saldo)
                self.serviceJugador.actualizar_saldo(jugador.jugador_id,(jugador.saldo-jugador.apuesta))
                print(f"Jugador {self.jugadores[i].nombre} sale de la mesa (PIERDE CONTRA LA CASA)")
            elif sumaJugador>sumaC and sumaJugador<=21:
                self.serviceJugador.agregar_jugadas(("GANO",str(jugador.apuesta)),jugador.jugador_id)
                self.serviceJugador.actualizar_saldo(jugador.jugador_id,(jugador.saldo+jugador.apuesta))
            else:
                self.serviceJugador.agregar_jugadas(("EMPATO",str(jugador.apuesta)),jugador.jugador_id)
                
            
            
    