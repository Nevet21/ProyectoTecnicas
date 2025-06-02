from Proyecto.models.Juego import Juego
import random
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.models.Jugador import Jugador

class BlackJack(Juego):
    def __init__(self, nombre, tipoJuego, jugadores):
        super().__init__(nombre, tipoJuego)
        self.jugadores = jugadores
        self.baraja = []  # Deck of cards
        self.cartasJugadores = []  # Stores the cards for each player
        self.crupier = []  # Dealer's cards
        self.serviceJugador = JugadorService()
        self.apuestas = {}  # Dictionary to store players' bets
    
    def apuesta(self):
        """Handles the initial bets of each player"""
        for jugador in self.jugadores:
                print(f"{jugador.nombre} su saldo es de: {jugador.saldo}")
                while True:
                    try:
                        apuesta = float(input(f"Ingrese su apuesta (máx {jugador.saldo}): "))
                        if apuesta <= 0 or apuesta > jugador.saldo:
                            print("Apuesta inválida. Intente nuevamente.")
                            continue
                        
                        # Store the bet and subtract it from the player's balance
                        self.apuestas[jugador.jugador_id] = apuesta
                        jugador.saldo -= apuesta
                        jugador.apuesta = apuesta
                        break
                    except ValueError:
                        print("Debe ingresar un número válido.")
    
    def crear_Mazo(self, baraja=None, aux=0, cartas=None, contador=0):
        """Creates a full deck of 52 cards using recursion"""
        if baraja is None:
            baraja = []
        if cartas is None:
            cartas = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        
        palos = ['♠', '♥', '♦', '♣']  # Suits
        
        if len(baraja) == 52:
            print("Terminó de barajar")
            self.baraja = baraja
            return baraja
        
        # Add current card (value + suit)
        baraja.append(f"{cartas[contador]}{palos[aux]}")
        
        if contador == 12:
            contador = 0
            aux += 1
        else:
            contador += 1
        
        return self.crear_Mazo(baraja, aux, cartas, contador)
    
    def barajar(self):
        """Shuffles the deck randomly"""
        random.shuffle(self.baraja)
        print("Baraja mezclada aleatoriamente")
        return self.baraja
    
    def repartirCarta(self, cartasJugador, canCartas):
        """Recursively deals a number of cards to a player"""
        if len(cartasJugador) == canCartas:
            return cartasJugador
        else:
            cartasJugador.append(self.baraja.pop(0))
            return self.repartirCarta(cartasJugador, canCartas)
        
    def repartirCartas(self):
        """Deals 2 cards to each player and the dealer"""
        for jugador in self.jugadores:
            cartas = self.repartirCarta([], 2)
            self.cartasJugadores.append((jugador, cartas))
        self.crupier = self.repartirCarta([], 2)
        print("CARTA CRUPIER: ")
        print(self.crupier[0])
        return self.cartasJugadores
    
    def seguirJugando(self):
        """Handles each player's turn to continue drawing or standing"""
        for i in range(len(self.jugadores)):
            jugador, cartas = self.cartasJugadores[i]
            
            while True:
                suma = self.calcular_suma_cartas(cartas)
                
                if suma > 21:
                    self.serviceJugador.agregar_jugadas(
                        ("Perdió", str(jugador.apuesta)), jugador.jugador_id
                    )
                    self.serviceJugador.actualizar_saldo(jugador.jugador_id, (jugador.saldo - jugador.apuesta))
                    print(f"Jugador {self.jugadores[i].nombre} sale de la mesa (Se pasó de 21)")
                    break
               
                opcion = input(f"{jugador.nombre}, ¿Quieres PEDIR (1) o PLANTARTE (2)? ").strip()
                
                if opcion == "1":
                    nueva_carta = self.repartirCarta([], 1)
                    cartas.extend(nueva_carta)
                    print(f"{jugador.nombre} recibe: {nueva_carta}. Cartas: {cartas} | Suma: {self.calcular_suma_cartas(cartas)}")
                    
                elif opcion == "2":
                    print(f"{jugador.nombre} se planta con: {cartas} | Suma: {suma}")
                    break
                    
                else:
                    print("Opción inválida. Ingresa 1 o 2.")
                
    def calcular_suma_cartas(self, cartas):
        """Calculates the total value of a hand, handling Aces as 1 or 11"""
        suma = 0
        ases = 0
        
        for carta in cartas:
            valor = carta[:-1]  # Remove suit symbol
            
            if valor in ['J', 'Q', 'K']:
                suma += 10
            elif valor == 'A':
                suma += 11
                ases += 1
            else:
                suma += int(valor)
        
        # Convert Aces from 11 to 1 if sum exceeds 21
        while suma > 21 and ases > 0:
            suma -= 10
            ases -= 1
        
        return suma

    def calcular_resultados(self):
        """Evaluates each player's hand against the dealer and updates balances"""
        suma_crupier = self.calcular_suma_cartas(self.crupier)
        resultados = []
        
        for jugador, cartas in self.cartasJugadores:
            suma_jugador = self.calcular_suma_cartas(cartas)
            apuesta = self.apuestas[jugador.jugador_id]
            
            if suma_jugador > 21:
                resultado = "PERDIO"
                ganancia = -apuesta
                jugador.juegos_perdidos += 1
            elif suma_crupier > 21 or suma_jugador > suma_crupier:
                resultado = "GANO"
                ganancia = apuesta * 2
                jugador.saldo += ganancia
                jugador.juegos_ganados += 1
            elif suma_jugador < suma_crupier:
                resultado = "PERDIO"
                ganancia = -apuesta
                jugador.juegos_perdidos += 1
            else:
                resultado = "EMPATO"
                ganancia = 0
                jugador.saldo += apuesta
            
            resultados.append({
                'jugador': jugador,
                'resultado': resultado,
                'ganancia': ganancia,
                'suma_jugador': suma_jugador,
                'suma_crupier': suma_crupier
            })
            
            jugador.agregar_jugada(f"BlackJack|{resultado}|{ganancia}")
        
        return resultados

    def turnoCrupiert(self):
        """Controls the dealer's turn: draws until reaching 17 or more"""
        suma = self.calcular_suma_cartas(self.crupier)
        while suma <= 16:
            cartaNueva = self.repartirCarta([], 1)
            self.crupier.extend(cartaNueva)
            suma = self.calcular_suma_cartas(self.crupier)
        
        return self.calcular_resultados()
                
    def gameOver(self, sumaC):
        """Final comparison if dealer doesn't bust, to determine winners/losers"""
        for i in range(len(self.cartasJugadores)):
            jugador, cartas = self.cartasJugadores[i]
            sumaJugador = self.calcular_suma_cartas(cartas)
            if sumaJugador < sumaC:
                self.serviceJugador.agregar_jugadas(("PERDIO", str(jugador.apuesta)), jugador.jugador_id)
                print(jugador.saldo)
                self.serviceJugador.actualizar_saldo(jugador.jugador_id, (jugador.saldo - jugador.apuesta))
                print(f"Jugador {self.jugadores[i].nombre} sale de la mesa (PIERDE CONTRA LA CASA)")
            elif sumaJugador > sumaC and sumaJugador <= 21:
                self.serviceJugador.agregar_jugadas(("GANO", str(jugador.apuesta)), jugador.jugador_id)
                self.serviceJugador.actualizar_saldo(jugador.jugador_id, (jugador.saldo + jugador.apuesta))
            else:
                self.serviceJugador.agregar_jugadas(("EMPATO", str(jugador.apuesta)), jugador.jugador_id)
