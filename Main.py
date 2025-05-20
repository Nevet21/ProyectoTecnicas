from Proyecto.models.Historial  import Historial
from Proyecto.models.Juego  import Juego
from Proyecto.models.Jugador import Jugador
from Proyecto.models.Mesa import Mesa
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.MesaService import MesaService
from Proyecto.CRUD_Entidades.JuegoService import JuegoService
from Proyecto.Busquedas.Busquedas import busquedaBinaria

def main():
    jugadorService= JugadorService()
    
    jugador=busquedaBinaria(1000,jugadorService.obtenerJugadores(),"saldo")
    
    jugador.mostrarInfo()
    
    

if __name__ == "__main__":
    main()
    