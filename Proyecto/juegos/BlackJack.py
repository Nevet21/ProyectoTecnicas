from Proyecto.models.Juego import Juego
import random
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.models.Jugador import Jugador

class blackJack(Juego):
    def __init__(self, nombre, tipoJuego, jugadores):
        # Hereda nombre y tipoJuego usando super()
        super().__init__(nombre, tipoJuego)
        # Atributo propio de BlackJack
        self.jugadores = jugadores
        self.baraja = []  # Inicializamos la baraja como atributo de la clase
        self.cartasJugadores=[]
        self.crupier=[]
        self.serviceJugador=JugadorService()
    
    def  apuesta(self):
        for jugador in self.jugadores:
            print(str(jugador.nombre)+ " su saldo es de: "+str(jugador.saldo))
            apuesta=int(input("Ingrese  su apuesta: "))
            if apuesta>jugador.saldo:
                print("no hay fondos disponibles  ")
            else:
                jugador.apuesta=apuesta
                
                
    
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


                    
    def turnoCrupiert(self):
        suma=self.calcular_suma_cartas(self.crupier)
        if suma<=16:
            cartaNueva=self.repartirCarta([],1)
            self.crupier.extend(cartaNueva)
        if suma>=17  and suma<=21:
            self.gameOver(suma)
        else:
            for i in range(len(self.cartasJugadores)):
                jugador, cartas = self.cartasJugadores[i]
                sumaJugador=self.calcular_suma_cartas(cartas)
                if sumaJugador<=21:
                    self.serviceJugador.agregar_jugadas(("GANO",str(jugador.apuesta)),jugador.jugador_id)
                    print("El jugador "+  str(jugador.nombre)+" GANO!!!")
                    self.serviceJugador.actualizar_saldo(jugador.jugador_id,(jugador.saldo+jugador.apuesta))
                    
                    
                
        
                        
                
            
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
                
            
            
    