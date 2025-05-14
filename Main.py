from models.Historial import Historial
from models.Juego  import Juego
from models.Jugador import Jugador
from models.Mesa import Mesa
from CRUD_Entidades.JugadorService import JugadorService
from CRUD_Entidades.MesaService import MesaService
from CRUD_Entidades.JuegoService import JuegoService

def main():
    mesa_service = MesaService()
    juego_service = JuegoService()
    jugador_service = JugadorService()
    

def test_jugador_service():
    # Crear una instancia del servicio
    jugador_service = JugadorService()
    

    # Crear nuevos jugadores
  
    jugador_service.crear_jugador("sergio",1000)
    
    



# Llamar a la función para probar
test_jugador_service()
