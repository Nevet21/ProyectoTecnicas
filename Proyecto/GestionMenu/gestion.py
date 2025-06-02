# Casino Management System - Main Application File
# Imports all necessary modules and classes for the casino system

import os
import sys
from Proyecto.models.Juego import Juego
from datetime import datetime
from Proyecto.Reportes.ReporteCasino import ReporteCasino
from Proyecto.CRUD_Entidades.JugadorService import JugadorService
from Proyecto.CRUD_Entidades.MesaService import MesaService
from Proyecto.CRUD_Entidades.HistorialService import HistorialService
from Proyecto.Busquedas_y_ordenamientos import burbuja, seleccion, insercion, mezcla
from Proyecto.juegos.BlackJack import BlackJack  # BlackJack game implementation
from Proyecto.juegos.DadoMentiroso import DadoMentiroso  # Liar's Dice game implementation
from Proyecto.CRUD_Entidades.JuegoService import JuegoService


def limpiar_pantalla():
    """Clears the console screen (cross-platform solution)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    """Displays the main menu options for the casino system"""
    print("\n=== MENÚ PRINCIPAL CASINO ===")
    print("1. Gestión de Jugadores")
    print("2. Gestión de Mesas")
    print("3. Gestión de Juegos")
    print("4. Jugar")
    print("5. Ver Historial")
    print("6. Reportes del Casino")
    print("0. Salir")

def mostrar_menu_jugadores():
    """Displays player management options"""
    print("\n=== GESTIÓN DE JUGADORES ===")
    print("1. Registrar nuevo jugador")
    print("2. Listar todos los jugadores")
    print("3. Buscar jugador por ID")
    print("4. Actualizar información de jugador")
    print("5. Eliminar jugador")
    print("0. Volver al menú principal")

def mostrar_menu_mesas():
    """Displays table management options"""
    print("\n=== GESTIÓN DE MESAS ===")
    print("1. Crear nueva mesa")
    print("2. Listar todas las mesas")
    print("3. Buscar mesa por ID")
    print("4. Modificar mesa")
    print("5. Eliminar mesa")
    print("6. Agregar jugador a mesa")
    print("7. Mover siguiente jugador a mesa")
    print("8. Ver cola de espera de mesa")
    print("0. Volver al menú principal")

def mostrar_menu_juegos():
    """Displays available game options"""
    print("\n=== JUEGOS DISPONIBLES ===")
    print("1. BlackJack")
    print("2. Dado Mentiroso")
    print("0. Volver al menú principal")

def mostrar_menu_historial():
    """Displays history viewing options"""
    print("\n=== HISTORIAL DE PARTIDAS ===")
    print("1. Ver historial completo")
    print("2. Buscar por jugador")
    print("0. Volver al menú principal")

def ver_reportes(reporte: ReporteCasino):
    """Handles casino report generation and display"""
    while True:
        print("\n=== MENÚ DE REPORTES ===")
        print("1. Jugadores con mayor saldo")
        print("2. Historial de un jugador")
        print("3. Jugadores con más victorias")
        print("4. Jugadores con más derrotas")
        print("5. Juegos con más participaciones")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            reporte.jugadores_mayor_saldo()
        elif opcion == "2":
            reporte.historial_jugador()
        elif opcion == "3":
            reporte.jugadores_mas_victorias()
        elif opcion == "4":
            reporte.jugadores_con_mas_perdidas()
        elif opcion == "5":
            reporte.juegos_mas_participados()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
        input("\nPresione Enter para continuar...")


def gestion_jugadores(jugador_service: JugadorService):
    """Handles all player management operations"""
    while True:
        mostrar_menu_jugadores()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Register new player
            limpiar_pantalla()
            print("\n--- REGISTRAR NUEVO JUGADOR ---")
            nombre = input("Nombre del jugador: ")
            saldo = float(input("Saldo inicial: $"))
            apuesta = float(input("Apuesta inicial: $"))
            jugador_service.crear_jugador(nombre, saldo, apuesta)
            print("Jugador registrado con éxito!")
            
        elif opcion == "2":
            # List all players
            limpiar_pantalla()
            print("\n--- LISTADO DE JUGADORES ---")
            jugadores = jugador_service.obtener_jugadores()
            for jugador in jugadores:
                jugador.mostrarInfo()
                print("--------------------")
                
        elif opcion == "3":
            # Search player by ID
            limpiar_pantalla()
            print("\n--- BUSCAR JUGADOR ---")
            jugador_id = input("ID del jugador a buscar (ej. J1): ")
            jugador = jugador_service.buscar_jugador(jugador_id=jugador_id)
            if jugador:
                jugador.mostrarInfo()
            else:
                print("Jugador no encontrado")
                
        elif opcion == "4":
            # Update player information
            limpiar_pantalla()
            print("\n--- ACTUALIZAR JUGADOR ---")
            jugador_id = input("ID del jugador a actualizar: ")
            jugador = jugador_service.buscar_jugador(jugador_id=jugador_id)
            if jugador:
                print("\nDeje en blanco los campos que no desea modificar")
                nuevo_nombre = input(f"Nuevo nombre ({jugador.nombre}): ") or None
                nuevo_saldo = input(f"Nuevo saldo ({jugador.saldo}): ")
                nuevo_saldo = float(nuevo_saldo) if nuevo_saldo else None
                nueva_apuesta = input(f"Nueva apuesta ({jugador.apuesta}): ")
                nueva_apuesta = float(nueva_apuesta) if nueva_apuesta else None
                
                if jugador_service.actualizar_jugador(
                    jugador_id=jugador_id,
                    nuevo_nombre=nuevo_nombre,
                    nuevo_saldo=nuevo_saldo,
                    nueva_apuesta=nueva_apuesta
                ):
                    print("Jugador actualizado!")
            else:
                print("Jugador no encontrado")
                
        elif opcion == "5":
            # Delete player
            limpiar_pantalla()
            print("\n--- ELIMINAR JUGADOR ---")
            jugador_id = input("ID del jugador a eliminar: ")
            if jugador_service.borrar_jugador(jugador_id=jugador_id):
                print("Jugador eliminado con éxito")
            else:
                print("No se pudo eliminar el jugador")
                
        elif opcion == "0":
            break
            
        else:
            print("Opción no válida")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

def gestion_mesas(mesa_service: MesaService, jugador_service: JugadorService):
    """Handles all table management operations"""
    while True:
        limpiar_pantalla()
        mostrar_menu_mesas()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Create new table
            limpiar_pantalla()
            print("\n--- CREAR NUEVA MESA ---")
            nombre_juego = input("Nombre del juego (ej. Ruleta, BlackJack, Dado Mentiroso): ").strip()
            
            try:
                can_jugadores = int(input("Capacidad máxima de jugadores: "))
                if can_jugadores <= 0:
                    print("Error: La capacidad debe ser mayor que 0")
                    input("\nPresione Enter para continuar...")
                    continue
            except ValueError:
                print("Error: Debe ingresar un número válido")
                input("\nPresione Enter para continuar...")
                continue
            
            # Create game instance based on name
            juego = None
            if nombre_juego.lower() == "blackjack":
                juego = BlackJack("Blackjack", "Cartas",can_jugadores)
            elif nombre_juego.lower() == "dado mentiroso":
                juego = DadoMentiroso()
                # Validate player limits for Liar's Dice
                if can_jugadores < juego.min_jugadores or can_jugadores > juego.max_jugadores:
                    print(f"Error: Dado Mentiroso requiere entre {juego.min_jugadores} y {juego.max_jugadores} jugadores")
                    input("\nPresione Enter para continuar...")
                    continue
            else:
                juego = Juego(nombre_juego, "Mesa")
            
            # Create the table
            mesa = mesa_service.crearMesa(juego, can_jugadores)
            if mesa:
                print(f"\nMesa {mesa.mesa_id} creada con éxito!")
                print(f"Juego: {juego.get_nombre()}")
                print(f"Capacidad: {can_jugadores} jugadores")
            else:
                print("\nNo se pudo crear la mesa")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            # List all tables
            limpiar_pantalla()
            print("\n--- LISTADO DE MESAS ---")
            if not mesa_service.mesas:
                print("No hay mesas creadas aún.")
            else:
                for mesa in mesa_service.mesas:
                    print(f"\nMesa ID: {mesa.mesa_id}")
                    print(f"Juego: {mesa.juego.get_nombre()}")
                    print(f"Capacidad: {len(mesa.jugadores)}/{mesa.canJugadores}")
                    print(f"Estado: {'Activa' if mesa.activa else 'Inactiva'}")
                    print("Jugadores en mesa:")
                    for jugador in mesa.jugadores:
                        print(f"- {jugador.nombre} (ID: {jugador.jugador_id})")
                    print("Jugadores en espera:", len(mesa.cola_espera))
                    print("--------------------")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "3":
            # Search table by ID
            limpiar_pantalla()
            print("\n--- BUSCAR MESA ---")
            mesa_id = input("ID de la mesa a buscar (ej. M1): ").strip()
            mesa = mesa_service.buscarMesa(mesa_id)
            if mesa:
                print(f"\nMesa ID: {mesa.mesa_id}")
                print(f"Juego: {mesa.juego.get_nombre()}")
                print(f"Capacidad: {len(mesa.jugadores)}/{mesa.canJugadores}")
                print(f"Estado: {'Activa' if mesa.activa else 'Inactiva'}")
                print("\nJugadores en mesa:")
                for jugador in mesa.jugadores:
                    print(f"- {jugador.nombre} (ID: {jugador.jugador_id})")
                print("\nJugadores en espera:")
                for i, jugador in enumerate(mesa.cola_espera, 1):
                    print(f"{i}. {jugador.nombre} (ID: {jugador.jugador_id})")
            else:
                print("\nMesa no encontrada")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            # Modify table
            limpiar_pantalla()
            print("\n--- MODIFICAR MESA ---")
            mesa_id = input("ID de la mesa a modificar: ").strip()
            mesa = mesa_service.buscarMesa(mesa_id)
            if not mesa:
                print("\nMesa no encontrada")
                input("\nPresione Enter para continuar...")
                continue
                
            print("\nDeje vacío para mantener el valor actual")
            nuevo_nombre = input(f"Nombre del juego ({mesa.juego.get_nombre()}): ").strip()
            nueva_capacidad = input(f"Capacidad ({mesa.canJugadores}): ")
            nuevo_estado = input(f"Activar/Desactivar [1/0] (Actual: {mesa.activa}): ")
            
            try:
                nueva_capacidad = int(nueva_capacidad) if nueva_capacidad else None
                if nueva_capacidad is not None and nueva_capacidad <= 0:
                    print("Error: La capacidad debe ser mayor que 0")
                    input("\nPresione Enter para continuar...")
                    continue
                    
                # Validate limits for Liar's Dice
                if isinstance(mesa.juego, DadoMentiroso) and nueva_capacidad is not None:
                    if nueva_capacidad < mesa.juego.min_jugadores or nueva_capacidad > mesa.juego.max_jugadores:
                        print(f"Error: Dado Mentiroso requiere entre {mesa.juego.min_jugadores} y {mesa.juego.max_jugadores} jugadores")
                        input("\nPresione Enter para continuar...")
                        continue
                
                nuevo_estado = bool(int(nuevo_estado)) if nuevo_estado else None
                
                if mesa_service.actualizarMesa(mesa_id, 
                        nombre_juego=nuevo_nombre or None,
                        canJugadores=nueva_capacidad,
                        activa=nuevo_estado):
                    print("\nMesa actualizada con éxito")
                else:
                    print("\nError al actualizar la mesa")
            except ValueError:
                print("\nError: Ingrese valores válidos")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "5":
            # Delete table
            limpiar_pantalla()
            print("\n--- ELIMINAR MESA ---")
            mesa_id = input("ID de la mesa a eliminar: ").strip()
            if mesa_service.borrarMesa(mesa_id):
                print("\nMesa eliminada con éxito")
            else:
                print("\nNo se encontró la mesa")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "6":
            # Add player to table
            limpiar_pantalla()
            print("\n--- AGREGAR JUGADOR A MESA ---")
            mesa_id = input("ID de la mesa: ").strip()
            jugador_id = input("ID del jugador: ").strip()
            
            jugador = jugador_service.buscar_jugador(jugador_id=jugador_id)
            if not jugador:
                print("\nJugador no encontrado")
                input("\nPresione Enter para continuar...")
                continue
                
            success, message = mesa_service.agregar_jugador_a_mesa(mesa_id, jugador)
            print(f"\n{message}")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "7":
            # Move next player from queue to table
            limpiar_pantalla()
            print("\n--- MOVER SIGUIENTE JUGADOR A MESA ---")
            mesa_id = input("ID de la mesa: ").strip()
            success, message = mesa_service.mover_siguiente_jugador(mesa_id)
            print(f"\n{message}")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "8":
            # View waiting queue
            limpiar_pantalla()
            print("\n--- COLA DE ESPERA DE MESA ---")
            mesa_id = input("ID de la mesa: ").strip()
            cola = mesa_service.obtener_cola_espera(mesa_id)
            if cola:
                print(f"\nJugadores en espera para mesa {mesa_id}:")
                for i, jugador in enumerate(cola, 1):
                    print(f"{i}. {jugador.nombre} (ID: {jugador.jugador_id})")
            else:
                print("\nNo hay jugadores en espera o mesa no encontrada")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "0":
            break
            
        else:
            print("\nOpción no válida")
            input("\nPresione Enter para continuar...")

def jugar(jugador_service: JugadorService, mesa_service: MesaService, historial_service: HistorialService):
    """Main game playing interface"""
    while True:
        limpiar_pantalla()
        mostrar_menu_juegos()
        opcion = input("Seleccione un juego: ")
        
        if opcion == "1":
            jugar_blackjack(jugador_service, mesa_service, historial_service)
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            jugar_dado_mentiroso(jugador_service, mesa_service, historial_service)
            input("\nPresione Enter para continuar...")
        elif opcion == "0":
            break
        else:
            print("Opción no válida")
            input("\nPresione Enter para continuar...")

def jugar_blackjack(jugador_service, mesa_service, historial_service):
    """Handles BlackJack game flow"""
    limpiar_pantalla()
    print("=== JUGAR BLACKJACK ===")

    # Find available BlackJack tables
    mesas_disponibles = [m for m in mesa_service.mesas if isinstance(m.juego, BlackJack) or m.juego.get_nombre().lower() == "blackjack"]
    if not mesas_disponibles:
        print("No hay mesas disponibles para BlackJack.")
        input("\nPresione Enter para volver...")
        return

    # Show available tables
    print("\nMesas disponibles para BlackJack:")
    for i, mesa in enumerate(mesas_disponibles, 1):
        print(f"{i}. Mesa {mesa.mesa_id} - Jugadores: {len(mesa.jugadores)}/{mesa.canJugadores}")

    try:
        seleccion = int(input("\nSeleccione una mesa: ")) - 1
        if seleccion < 0 or seleccion >= len(mesas_disponibles):
            print("Selección inválida.")
            input("\nPresione Enter para volver...")
            return
    except ValueError:
        print("Debe ingresar un número válido.")
        input("\nPresione Enter para volver...")
        return

    mesa_seleccionada = mesas_disponibles[seleccion]
    
    # Verify minimum players
    if len(mesa_seleccionada.jugadores) < 2:
        print("\nSe necesitan al menos 2 jugadores para jugar BlackJack.")
        input("\nPresione Enter para volver...")
        return

    # Create BlackJack instance
    blackjack = BlackJack(
        nombre="BlackJack",
        tipoJuego="Cartas",
        jugadores=mesa_seleccionada.jugadores
    )

    # Game setup
    blackjack.crear_Mazo()
    blackjack.barajar()
    
    # Place initial bets
    print("\n--- Realizando apuestas iniciales ---")
    blackjack.apuesta()

    # Save initial balances for history
    saldos_iniciales = {j.jugador_id: j.saldo for j in blackjack.jugadores}

    # Deal initial cards
    blackjack.repartirCartas()

    # Show initial cards
    print("\nCartas del Crupier:")
    print(f"{blackjack.crupier[0]} y [Carta oculta]")

    # Player turns
    for jugador, cartas in blackjack.cartasJugadores:
        print(f"\n--- Turno de {jugador.nombre} ---")
        print(f"Cartas: {cartas}")
        suma_actual = blackjack.calcular_suma_cartas(cartas)
        print(f"Suma actual: {suma_actual}")

        while True:
            opcion = input("¿Quieres PEDIR (1) o PLANTARTE (2)? ").strip()
            if opcion == "1":
                nueva_carta = blackjack.repartirCarta([], 1)
                cartas.extend(nueva_carta)
                print(f"\nRecibiste: {nueva_carta}")
                print(f"Cartas actuales: {cartas}")
                suma_actual = blackjack.calcular_suma_cartas(cartas)
                print(f"Suma actual: {suma_actual}")
                
                if suma_actual > 21:
                    print("¡Te pasaste de 21!")
                    break
            elif opcion == "2":
                print(f"{jugador.nombre} se planta con {suma_actual} puntos")
                break
            else:
                print("Opción inválida.")

    # Dealer turn and results
    print("\n--- Turno del Crupier ---")
    print(f"Cartas del Crupier: {blackjack.crupier}")
    resultados = blackjack.turnoCrupiert()
    suma_crupier = blackjack.calcular_suma_cartas(blackjack.crupier)
    print(f"Suma final del Crupier: {suma_crupier}")

    # Determine winners
    ganadores = []
    perdedores = []
    empatados = []
    
    for res in resultados:
        if res['resultado'] == "GANO":
            ganadores.append(res['jugador'].nombre)
        elif res['resultado'] == "PERDIO":
            perdedores.append(res['jugador'].nombre)
        else:
            empatados.append(res['jugador'].nombre)

    # Prepare winner text for history
    if suma_crupier > 21:
        ganador_texto = "Jugadores: " + ", ".join(ganadores) if ganadores else "Crupier (todos perdieron)"
    elif ganadores:
        ganador_texto = "Jugadores: " + ", ".join(ganadores)
    else:
        ganador_texto = "Crupier"

    # Show game summary
    print("\n=== RESUMEN DE LA PARTIDA ===")
    if suma_crupier > 21:
        print("\n¡EL CRUPIER SE PASÓ DE 21!")
        if ganadores:
            print("¡GANADORES CONTRA LA CASA:")
            for ganador in ganadores:
                print(f"- {ganador}")
        else:
            print("¡PERO TODOS LOS JUGADORES TAMBIÉN PERDIERON!")
    elif ganadores:
        print("\n¡GANADORES CONTRA EL CRUPIER:")
        for ganador in ganadores:
            print(f"- {ganador}")
    else:
        print("\n¡EL CRUPIER GANA LA RONDA!")

    # Show player details
    print("\nDETALLE POR JUGADOR:")
    for res in resultados:
        jugador = res['jugador']
        print(f"\n{jugador.nombre.upper()}:")
        print(f"- Cartas finales: {res.get('cartas', ['No disponibles'])}")
        print(f"- Puntos: {res['suma_jugador']}")
        print(f"- Resultado: {res['resultado']}")
        print(f"- Ganancia/Perdida: {'+' if res['ganancia'] >=0 else ''}{res['ganancia']}")
        print(f"- Nuevo saldo: ${jugador.saldo}")

    # Prepare history
    historial = historial_service.crearHistorial(mesa_seleccionada)
    resultado_historial = {
        "juego": "BlackJack",
        "crupier_sum": suma_crupier,
        "ganador": ganador_texto,
        "jugadores": {}
    }

    for res in resultados:
        jugador = res['jugador']
        resultado_historial["jugadores"][jugador.jugador_id] = {
            "nombre": jugador.nombre,
            "resultado": res['resultado'],
            "ganancia": res['ganancia'],
            "suma_jugador": res['suma_jugador'],
            "cartas": res.get('cartas', [])
        }

        # Add to player's personal history
        jugador.agregar_historial({
            "historial_id": historial.get_historial_id(),
            "juego": "BlackJack",
            "resultado": res['resultado'],
            "saldo_cambiado": res['ganancia'],
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "puntos": res['suma_jugador'],
            "puntos_crupier": suma_crupier,
            "ganador_partida": ganador_texto
        })

    # Save everything
    historial.set_resultado(resultado_historial)
    historial_service._guardar_historiales()
    jugador_service._guardar_jugadores()

    input("\nPresione Enter para volver al menú principal...")


def jugar_dado_mentiroso(jugador_service: JugadorService, mesa_service: MesaService, historial_service: HistorialService):
    """Handles Liar's Dice game flow"""
    # Find available Liar's Dice tables
    mesas_disponibles = []
    for mesa in mesa_service.mesas:
        # Check if table has a valid game
        if (hasattr(mesa, 'juego') and mesa.juego and mesa.activa):
            # For pre-loaded games
            if isinstance(mesa.juego, DadoMentiroso):
                mesas_disponibles.append(mesa)
            # For games loaded from file (may come as generic Juego)
            elif mesa.juego.get_nombre().lower() == "dado mentiroso":
                # Convert to DadoMentiroso if needed
                mesa.juego = DadoMentiroso()
                mesas_disponibles.append(mesa)
    
    if not mesas_disponibles:
        print("\nNo hay mesas disponibles para Dado Mentiroso.")
        print("Por favor crea una mesa desde el menú de gestión de mesas.")
        input("\nPresione Enter para volver...")
        return
    
    print("\n=== MESAS DISPONIBLES PARA DADO MENTIROSO ===")
    for i, mesa in enumerate(mesas_disponibles, 1):
        print(f"\n{i}. Mesa ID: {mesa.mesa_id}")
        print(f"   Juego: {mesa.juego.get_nombre()}")
        print(f"   Capacidad: {len(mesa.jugadores)}/{mesa.canJugadores} jugadores")
        print(f"   Estado: {'Activa' if mesa.activa else 'Inactiva'}")
        
        if mesa.jugadores:
            print("   Jugadores en mesa:")
            for jugador in mesa.jugadores:
                print(f"   - {jugador.nombre} (ID: {jugador.jugador_id}) - Saldo: ${jugador.saldo}")
        else:
            print("   No hay jugadores en la mesa")
        
        if hasattr(mesa, 'cola_espera') and mesa.cola_espera:
            print(f"   Jugadores en espera: {len(mesa.cola_espera)}")
    
    try:
        seleccion = int(input("\nSeleccione una mesa (número): ")) - 1
        if 0 <= seleccion < len(mesas_disponibles):
            mesa_seleccionada = mesas_disponibles[seleccion]
            
            # Verify minimum players
            if len(mesa_seleccionada.jugadores) < mesa_seleccionada.juego.min_jugadores:
                print(f"\nSe necesitan al menos {mesa_seleccionada.juego.min_jugadores} jugadores para comenzar.")
                print(f"Actualmente hay {len(mesa_seleccionada.jugadores)} jugadores en la mesa.")
                
                # Option to add players
                print("\n1. Agregar jugadores a esta mesa")
                print("2. Volver al menú anterior")
                opcion = input("Seleccione una opción: ")
                
                if opcion == "1":
                    jugadores_disponibles = [j for j in jugador_service.obtener_jugadores() 
                        if j not in mesa_seleccionada.jugadores]
                    
                    if not jugadores_disponibles:
                        print("\nNo hay jugadores disponibles para agregar.")
                        input("\nPresione Enter para volver...")
                        return
                    
                    print("\nJugadores disponibles:")
                    for i, jugador in enumerate(jugadores_disponibles, 1):
                        print(f"{i}. {jugador.nombre} (ID: {jugador.jugador_id}) - Saldo: ${jugador.saldo}")
                    
                    try:
                        seleccion_jugador = int(input("\nSeleccione un jugador para agregar (número): ")) - 1
                        if 0 <= seleccion_jugador < len(jugadores_disponibles):
                            jugador = jugadores_disponibles[seleccion_jugador]
                            success, message = mesa_service.agregar_jugador_a_mesa(mesa_seleccionada.mesa_id, jugador)
                            print(message)
                            
                            if len(mesa_seleccionada.jugadores) >= mesa_seleccionada.juego.min_jugadores:
                                print("\n¡Ahora hay suficientes jugadores para comenzar!")
                            else:
                                print("\nAún no hay suficientes jugadores.")
                            input("\nPresione Enter para continuar...")
                        else:
                            print("\nSelección no válida")
                            input("\nPresione Enter para volver...")
                            return
                    except ValueError:
                        print("\nPor favor ingrese un número válido")
                        input("\nPresione Enter para volver...")
                        return
                else:
                    return
            
            # Save initial balances for history
            saldos_iniciales = {j.jugador_id: j.saldo for j in mesa_seleccionada.jugadores}
            
            # Start the game
            juego = mesa_seleccionada.juego
            if not juego.iniciar_partida(mesa_seleccionada, historial_service):
                print("\nNo se pudo iniciar el juego.")
                input("\nPresione Enter para volver...")
                return
            
            # Main game loop
            while True:
                limpiar_pantalla()
                jugador_actual = juego.jugadores[juego.turno_actual]
                estado = juego.obtener_estado(jugador_actual.jugador_id)
                
                # Show game information
                print(f"\n=== MESA {mesa_seleccionada.mesa_id} - DADO MENTIROSO ===")
                print(f"=== Turno de: {jugador_actual.nombre} ===")
                print(f"\nSaldo actual: ${jugador_actual.saldo}")
                print(f"Tus dados: {estado['tus_dados']}")
                
                print("\nEstado de los jugadores:")
                for jugador_info in estado['jugadores']:
                    print(f"- {jugador_info['nombre']}: {jugador_info['dados_restantes']} dados | Saldo: ${jugador_info['saldo']}")
                
                if estado['ultima_apuesta']:
                    cantidad, valor = estado['ultima_apuesta']
                    print(f"\nÚltima apuesta: {cantidad} dados de valor {valor}")
                
                print("\nOpciones:")
                print("1. Hacer apuesta normal")
                print("2. Hacer apuesta segura")
                print("3. Desconfiar")
                print("4. Ver historial reciente")
                print("5. Obtener recomendación de estrategia")
                print("0. Salir del juego")
                
                opcion = input("\nSeleccione una opción: ")
                
                if opcion == "1":
                    try:
                        print("\n--- HACER APUESTA ---")
                        valor = int(input("Valor del dado (1-6): "))
                        if valor < 1 or valor > 6:
                            print("Error: El valor debe estar entre 1 y 6")
                            input("\nPresione Enter para continuar...")
                            continue
                            
                        cantidad = int(input("Cantidad total de dados: "))
                        if cantidad < 1:
                            print("Error: La cantidad debe ser al menos 1")
                            input("\nPresione Enter para continuar...")
                            continue
                            
                        success, mensaje = juego.hacer_apuesta(jugador_actual.jugador_id, cantidad, valor)
                        print(mensaje)
                    except ValueError:
                        print("Error: Debes ingresar números válidos")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "2":
                    try:
                        print("\n--- HACER APUESTA SEGURA ---")
                        valor = int(input("Valor del dado (1-6): "))
                        if valor < 1 or valor > 6:
                            print("Error: El valor debe estar entre 1 y 6")
                            input("\nPresione Enter para continuar...")
                            continue
                            
                        cantidad = int(input("Cantidad exacta de dados: "))
                        if cantidad < 1:
                            print("Error: La cantidad debe ser al menos 1")
                            input("\nPresione Enter para continuar...")
                            continue
                            
                        success, mensaje = juego.hacer_apuesta(jugador_actual.jugador_id, cantidad, valor, True)
                        print(mensaje)
                        
                        if success and juego._verificar_ganador():
                            jugador_service._guardar_jugadores()
                            break
                    except ValueError:
                        print("Error: Debes ingresar números válidos")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "3":
                    if not juego.ultima_apuesta:
                        print("\nNo hay apuesta para desconfiar")
                        input("\nPresione Enter para continuar...")
                        continue
                        
                    confirmacion = input(f"\n¿Estás seguro que quieres desconfiar? (s/n): ").lower()
                    if confirmacion != 's':
                        continue
                        
                    success, mensaje = juego.desconfiar(jugador_actual.jugador_id)
                    print(mensaje)
                    
                    if success and juego._verificar_ganador():
                        jugador_service._guardar_jugadores()
                        break
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "4":
                    print("\n--- HISTORIAL RECIENTE ---")
                    if 'historial' in estado and estado['historial']:
                        for evento in estado['historial'][-5:]:
                            print(f"- {evento}")
                    else:
                        print("No hay eventos registrados aún")
                    input("\nPresione Enter para continuar...")

                elif opcion == "5":
                    print("\n--- RECOMENDACIÓN DE ESTRATEGIA ---")
                    recomendaciones = juego.obtener_estrategia_recomendada(jugador_actual.jugador_id)
                    if recomendaciones:
                        print("\nSecuencia recomendada de apuestas:")
                        for i, (apuesta, es_segura) in enumerate(recomendaciones, 1):
                            cantidad, valor = apuesta
                            tipo = "Segura" if es_segura else "Normal"
                            print(f"{i}. Apostar {cantidad} dados de valor {valor} ({tipo})")
                    else:
                        print("\nNo hay recomendaciones disponibles en este momento.")
                    input("\nPresione Enter para continuar...")
                
                elif opcion == "0":
                    print("\nSaliendo del juego...")
                    jugador_service._guardar_jugadores()
                    break
                
                else:
                    print("\nOpción no válida")
                    input("\nPresione Enter para continuar...")
            
            # Mostrar resumen final si el juego terminó
            if juego._verificar_ganador():
                ganador = next(j for j in juego.jugadores if len(juego.dados_jugadores[j.jugador_id]) > 0)
                print(f"\n¡¡¡ {ganador.nombre} HA GANADO LA PARTIDA !!!")
                
                print("\nResumen final:")
                # Buscar historial asociado a esta mesa
                historial = historial_service.historiales[-1] if historial_service.historiales else None
                if historial and historial.get_mesa().mesa_id == mesa_seleccionada.mesa_id:
                    resultado = {
                        "juego": mesa_seleccionada.juego.get_nombre(),
                        "nombre_ganador": ganador.nombre,
                        "jugadores": {}
                    }

                    for jugador in juego.jugadores:
                        es_ganador = jugador == ganador
                        resultado["jugadores"][jugador.jugador_id] = {
                            "nombre": jugador.nombre,
                            "resultado": "GANADOR" if es_ganador else "PERDEDOR",
                            "ganancia": jugador.saldo - saldos_iniciales[jugador.jugador_id]
                        }

                        # 🟢 ACTUALIZAR estadísticas del jugador
                        if es_ganador:
                            jugador.juegos_ganados += 1
                        else:
                            jugador.juegos_perdidos += 1

                    historial.set_resultado(resultado)
                    historial_service._guardar_historiales()
                    jugador_service._guardar_jugadores()


                for jugador in juego.jugadores:
                    dados_restantes = len(juego.dados_jugadores[jugador.jugador_id])
                    cambio_saldo = jugador.saldo - saldos_iniciales[jugador.jugador_id]
                    print(f"- {jugador.nombre}: {dados_restantes} dados | Saldo: ${jugador.saldo} ({'+' if cambio_saldo >=0 else ''}{cambio_saldo})")
        
        else:
            print("\nSelección no válida")
    except ValueError:
        print("\nError: Debe ingresar un número válido")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
    
    input("\nPresione Enter para volver al menú principal...")

def ver_historial(historial_service: HistorialService):
    while True:
        limpiar_pantalla()  # Clear the screen
        mostrar_menu_historial()  # Show the history menu
        opcion = input("Seleccione una opción: ")  # Ask the user to select an option
        
        if opcion == "1":
            limpiar_pantalla()  # Clear the screen
            print("\n=== HISTORIAL COMPLETO ===")  # Display full history title
            historiales = historial_service.historiales  # Retrieve all history records

            if not historiales:
                print("No hay registros en el historial.")  # No history found
            else:
                for hist in historiales:
                    # Print the history ID and associated table ID
                    print(f"\nID: {hist.get_historial_id()} | Mesa: {hist.get_mesa().mesa_id}")
                    # Check if 'resultado' attribute exists before printing final balance
                    if hasattr(hist, 'resultado'):
                        print(f"Saldo final: {hist.resultado.get('saldo_final', 'N/A')}")
        
        elif opcion == "2":
            jugador_id = input("Ingrese el ID del jugador: ").strip()  # Request player ID
            historial_jugador = historial_service.obtener_historial_por_jugador(jugador_id)  # Get player's history

            print(f"\n=== HISTORIAL DEL JUGADOR {jugador_id} ===")  # Display title
            if not historial_jugador:
                print("No se encontraron registros.")  # No records for this player
            else:
                for hist in historial_jugador:
                    hist.mostrar_info()  # Show detailed history info
                    print("-" * 50)  # Divider line

        elif opcion == "3":
            mesa_id = input("ID de la mesa a buscar: ")  # Ask for table ID
            print("\nResultados para la mesa:", mesa_id)
            arreglo=historial_service.obtener_historial_por_mesa(mesa_id)
            for opcion in arreglo:
                print(opcion.mostrar_info)
        
        
        elif opcion == "0":
            break  # Exit the history menu
            
        else:
            print("Opción no válida")  # Invalid option entered
        
        input("\nPresione Enter para continuar...")  # Pause before returning to menu


def gestion_juegos(juego_service: JuegoService):
    """
    Interactive menu for managing casino games.

    Options:
    1. Register new game
    2. List all games
    3. Search game by ID
    4. Update game
    5. Delete game
    0. Exit to main menu
    """
    while True:
        print("\n===== MENÚ DE GESTIÓN DE JUEGOS =====")
        print("1. Registrar nuevo juego")
        print("2. Listar todos los juegos")
        print("3. Buscar juego por ID")
        print("4. Actualizar juego")
        print("5. Eliminar juego")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Register a new game
            limpiar_pantalla()
            print("\n--- REGISTRAR NUEVO JUEGO ---")
            nombre = input("Nombre del juego: ")
            tipo = input("Tipo de juego (ej. Cartas, Dados, Tragamonedas): ")
            juego_service.crearJuego(nombre, tipo)

        elif opcion == "2":
            # List all games
            limpiar_pantalla()
            print("\n--- LISTADO DE JUEGOS ---")
            for juego in juego_service.juegos:
                print(f"ID: {juego.juego_id}, Nombre: {juego.get_nombre()}, Tipo: {juego.get_tipoJuego()}")
                print("--------------------")

        elif opcion == "3":
            # Search game by ID
            limpiar_pantalla()
            print("\n--- BUSCAR JUEGO ---")
            juego_id = input("ID del juego a buscar (ej. J1): ")
            juego_service.buscarJuego(juego_id)

        elif opcion == "4":
            # Update game information
            limpiar_pantalla()
            print("\n--- ACTUALIZAR JUEGO ---")
            juego_id = input("ID del juego a actualizar: ")
            juego = juego_service.buscarJuego(juego_id)
            if juego:
                print("\nDeje en blanco los campos que no desea modificar")
                nuevo_nombre = input(f"Nuevo nombre ({juego.get_nombre()}): ") or None
                nuevo_tipo = input(f"Nuevo tipo ({juego.get_tipoJuego()}): ") or None
                juego_service.actualizarJuego(juego_id, nombre=nuevo_nombre, tipoJuego=nuevo_tipo)

        elif opcion == "5":
            # Delete game
            limpiar_pantalla()
            print("\n--- ELIMINAR JUEGO ---")
            juego_id = input("ID del juego a eliminar: ")
            juego_service.borrarJuego(juego_id)

        elif opcion == "0":
            # Exit to main menu
            break

        else:
            # Invalid option
            print("Opción no válida")

        input("\nPresione Enter para continuar...")
        limpiar_pantalla()
