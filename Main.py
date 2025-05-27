from Proyecto.models.Historial  import Historial
from Proyecto.models.Juego  import Juego
from Proyecto.models.Jugador import Jugador
from Proyecto.models.Mesa import Mesa
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.MesaService import MesaService
from Proyecto.CRUD_Entidades.JuegoService import JuegoService
from Proyecto.CRUD_Entidades.HistorialService import HistorialService
from Proyecto.Busquedas.Busquedas import busquedaBinaria
from Proyecto.juegos.BlackJack import blackJack


from Proyecto.models.Juego import Juego
from Proyecto.models.Jugador import Jugador
from Proyecto.CRUD_Entidades.JugadorService import JugadorService

from Proyecto.models.Jugador import Jugador
from Proyecto.models.Juego import Juego
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
import uuid
from Proyecto.models.Juego import Juego
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
import uuid

def main():
    print("¡Bienvenido al Casino - Juego de Blackjack!")
    print("------------------------------------------\n")
    
    # Configuración inicial de jugadores
    service=JugadorService()
    jugadores=service.obtener_jugadores()
    
    # Inicializar el juego
    juego = blackJack(
        nombre="Blackjack", 
        tipoJuego="Cartas", 
        jugadores=jugadores
    )
    
    # Preparar el juego
    print("\nPreparando el juego...")
    juego.crear_Mazo()
    juego.barajar()
    
    # Fase de apuestas
    print("\n--- Fase de Apuestas ---")
    juego.apuesta()
    
    # Repartir cartas iniciales
    print("\nRepartiendo cartas...")
    juego.repartirCartas()
    
    # Mostrar situación inicial
    print("\n--- Situación Inicial ---")
    print(f"Crupier: [{'?', juego.crupier[0]}]")  # Mostramos solo una carta del crupier
    
    for jugador, cartas in juego.cartasJugadores:
        suma = juego.calcular_suma_cartas(cartas)
        print(f"{jugador.nombre}: {cartas} | Suma: {suma} | Apuesta: ${jugador.apuesta}")
    
    # Turno de los jugadores
    print("\n--- Turno de los Jugadores ---")
    juego.seguirJugando()
    
    # Turno del crupier
    print("\n--- Turno del Crupier ---")
    print(f"Cartas del crupier: {juego.crupier}")
    juego.turnoCrupiert()
    
    # Resultados finales
    print("\n--- Resultados Finales ---")
    suma_crupier = juego.calcular_suma_cartas(juego.crupier)
    print(f"Crupier: {juego.crupier} | Suma: {suma_crupier}")
    
    
    jugador.mostrarInfo()  # Mostramos información completa del jugador

if __name__ == "__main__":
    main()