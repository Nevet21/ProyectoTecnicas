from Proyecto.Reportes.ReporteCasino import ReporteCasino
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.MesaService import MesaService
from Proyecto.CRUD_Entidades.JuegoService import JuegoService
from Proyecto.CRUD_Entidades.HistorialService import HistorialService
from Proyecto.GestionMenu.gestion import (
    limpiar_pantalla,
    mostrar_menu_principal,
    gestion_jugadores,
    gestion_mesas,
    jugar,
    ver_historial,
    ver_reportes,
    gestion_juegos
)

def main():
    # Initialize services
    jugador_service = JugadorService()
    mesa_service = MesaService()
    historial_service = HistorialService()
    juego_service = JuegoService()

    # Instantiate the reporting class
    reporte = ReporteCasino(jugador_service, historial_service, juego_service)

    # Load players into tables
    mesa_service.cargar_jugadores_en_mesas(jugador_service)
    
    while True:
        limpiar_pantalla()
        print("¡Bienvenido al Sistema de Casino!")  # Welcome to the Casino System!
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")  # Select an option
        
        if opcion == "1":
            gestion_jugadores(jugador_service)
            
        elif opcion == "2":
            gestion_mesas(mesa_service, jugador_service)
            
        elif opcion == "3":
           gestion_juegos(juego_service)
        elif opcion == "4":
            jugar(jugador_service, mesa_service, historial_service)
            
        elif opcion == "5":
            ver_historial(historial_service)
            
        elif opcion == "6":
            ver_reportes(reporte)

        else:
            print("Opción no válida. Intente nuevamente.")  # Invalid option. Please try again.
            input("Presione Enter para continuar...")  # Press Enter to continue...

if __name__ == "__main__":
    main()
