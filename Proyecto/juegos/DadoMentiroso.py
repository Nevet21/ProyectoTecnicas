from datetime import datetime
from Proyecto.models.Juego import Juego
from Proyecto.models.Mesa import Mesa
import random
from Proyecto.juegos.EstrategiaDadoMentiroso import EstrategiaDadoMentiroso
from typing import List, Tuple

class DadoMentiroso(Juego):
    def __init__(self):
        super().__init__("Dado Mentiroso", "Dados")
        self.min_jugadores = 2
        self.max_jugadores = 6
        self.APUESTA_BASE = 50
        self.PREMIO_GANADOR = 100
        self.PENALIZACION_PERDEDOR = 30
        self.dados_jugadores = {}
        self.turno_actual = 0
        self.ultima_apuesta = None
        self.resultados_jugadores = {}  # Diccionario para acumular resultados {jugador_id: balance}

    def repartir_dados_iniciales(self):
        """Reparte 5 dados iniciales a cada jugador"""
        self.dados_jugadores = {
            jugador.jugador_id: [random.randint(1, 6) for _ in range(5)]
            for jugador in self.jugadores
        }
        # Inicializar el registro de resultados
        self.resultados_jugadores = {jugador.jugador_id: 0 for jugador in self.jugadores}

    def _actualizar_dados_todos(self):
        """Actualiza TODOS los dados de TODOS los jugadores aleatoriamente"""
        for jugador_id in self.dados_jugadores:
            cantidad_dados = len(self.dados_jugadores[jugador_id])
            if cantidad_dados > 0:
                self.dados_jugadores[jugador_id] = [random.randint(1, 6) for _ in range(cantidad_dados)]

    def iniciar_partida(self, mesa: Mesa, historial_service):
        """Inicia una nueva partida"""
        if not mesa or len(mesa.jugadores) < self.min_jugadores:
            return False
        
        self.mesa = mesa
        self.jugadores = mesa.jugadores
        self.historial_service = historial_service
        self.turno_actual = 0
        self.repartir_dados_iniciales()
        self.ultima_apuesta = None
        
        self.historial_service.crearHistorial(mesa)
        return True

    def _registrar_resultado(self, jugador_id, cantidad, es_ganador=False):
        """
        Registra el resultado financiero de un jugador
        Args:
            jugador_id: ID del jugador
            cantidad: Monto a registrar
            es_ganador: True si es ganancia, False si es pérdida
        """
        if es_ganador:
            self.resultados_jugadores[jugador_id] += cantidad
        else:
            self.resultados_jugadores[jugador_id] -= cantidad

    def _siguiente_turno(self):
        """Avanza al siguiente turno"""
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)

    def _contar_dados_mesa(self, jugadores=None, total_dados=None, index=0):
        """
        Cuenta recursivamente todos los dados en juego
        Args:
            jugadores: Lista de jugadores (se auto-provee en llamadas recursivas)
            total_dados: Diccionario acumulador (se auto-provee)
            index: Índice del jugador actual (se auto-provee)
        Returns:
            Diccionario con el conteo de dados por valor {1: 3, 2: 5, ...}
        """
        # Inicialización en la primera llamada
        if jugadores is None:
            jugadores = self.jugadores
        if total_dados is None:
            total_dados = {}
        
        # Caso base: hemos procesado todos los jugadores
        if index >= len(jugadores):
            return total_dados
        
        jugador = jugadores[index]
        
        # Procesar dados del jugador actual
        for dado in self.dados_jugadores[jugador.jugador_id]:
            total_dados[dado] = total_dados.get(dado, 0) + 1
        
        # Llamada recursiva para el siguiente jugador
        return self._contar_dados_mesa(jugadores, total_dados, index + 1)

    def hacer_apuesta(self, jugador_id, cantidad, valor, es_segura=False):
        """Realiza una apuesta normal o segura"""
        jugador_actual = self.jugadores[self.turno_actual]
        if jugador_id != jugador_actual.jugador_id:
            return False, "No es tu turno"
        
        if valor < 1 or valor > 6:
            return False, "El valor del dado debe estar entre 1 y 6"
        
        if es_segura:
            return self._apuesta_segura(jugador_id, cantidad, valor)
        
        if self.ultima_apuesta:
            ultima_cant, ultimo_val = self.ultima_apuesta
            if cantidad < ultima_cant or (cantidad == ultima_cant and valor <= ultimo_val):
                return False, "Debes aumentar la cantidad o el valor del dado"
        
        self.ultima_apuesta = (cantidad, valor)
        mensaje = f"{jugador_actual.nombre} apuesta {cantidad} dados de {valor}"
        self._siguiente_turno()
        return True, mensaje

    def _apuesta_segura(self, jugador_id, cantidad, valor):
        """Maneja una apuesta segura con verificación exacta"""
        total_dados = self._contar_dados_mesa()
        conteo_real = total_dados.get(valor, 0)
        jugador = next(j for j in self.jugadores if j.jugador_id == jugador_id)
        
        if conteo_real == cantidad:
            # Apuesta correcta - todos pierden un dado
            for j in self.jugadores:
                if self.dados_jugadores[j.jugador_id]:
                    self.dados_jugadores[j.jugador_id].pop()
                
                if j.jugador_id == jugador_id:
                    j.saldo += self.PREMIO_GANADOR
                    self._registrar_resultado(j.jugador_id, self.PREMIO_GANADOR, True)
                else:
                    j.saldo = max(0, j.saldo - self.PENALIZACION_PERDEDOR)
                    self._registrar_resultado(j.jugador_id, self.PENALIZACION_PERDEDOR, False)
            
            self._actualizar_dados_todos()
            mensaje = f"¡Correcto! Había {conteo_real} dados de {valor}"
        else:
            # Apuesta incorrecta - jugador pierde un dado
            if self.dados_jugadores[jugador_id]:
                self.dados_jugadores[jugador_id].pop()
            
            perdida = self.PENALIZACION_PERDEDOR * 2
            jugador.saldo = max(0, jugador.saldo - perdida)
            self._registrar_resultado(jugador_id, perdida, False)
            self._actualizar_dados_todos()
            mensaje = f"¡Incorrecto! Había {conteo_real} dados de {valor}"
        
        self._verificar_ganador()
        self._siguiente_turno()
        return True, mensaje

    def desconfiar(self, jugador_id):
        """Maneja la acción de desconfiar de una apuesta"""
        if jugador_id != self.jugadores[self.turno_actual].jugador_id:
            return False, "No es tu turno"
        
        if not self.ultima_apuesta:
            return False, "No hay apuesta para desconfiar"
        
        cantidad, valor = self.ultima_apuesta
        total_dados = self._contar_dados_mesa()
        conteo_real = total_dados.get(valor, 0)
        
        jugador_actual = self.jugadores[self.turno_actual]
        jugador_anterior = self.jugadores[(self.turno_actual - 1) % len(self.jugadores)]
        
        # Construir el mensaje con los dados revelados
        mensaje_dados = "\n=== DADOS REVELADOS ===\n"
        for jugador in self.jugadores:
            mensaje_dados += f"{jugador.nombre}: {self.dados_jugadores[jugador.jugador_id]}\n"
        mensaje_dados += f"\nTotal de dados de {valor}: {conteo_real}\n"
        
        if conteo_real >= cantidad:
            # Desconfianza incorrecta - jugador actual pierde un dado
            if self.dados_jugadores[jugador_actual.jugador_id]:
                self.dados_jugadores[jugador_actual.jugador_id].pop()
            
            jugador_actual.saldo = max(0, jugador_actual.saldo - self.PENALIZACION_PERDEDOR)
            jugador_anterior.saldo += self.APUESTA_BASE
            
            self._registrar_resultado(jugador_actual.jugador_id, self.PENALIZACION_PERDEDOR, False)
            self._registrar_resultado(jugador_anterior.jugador_id, self.APUESTA_BASE, True)
            
            resultado = f"{mensaje_dados}¡Error! Había {conteo_real} dados de {valor}. {jugador_actual.nombre} pierde un dado."
        else:
            # Desconfianza correcta - jugador anterior pierde un dado
            if self.dados_jugadores[jugador_anterior.jugador_id]:
                self.dados_jugadores[jugador_anterior.jugador_id].pop()
            
            jugador_anterior.saldo = max(0, jugador_anterior.saldo - self.PENALIZACION_PERDEDOR)
            jugador_actual.saldo += self.APUESTA_BASE
            
            self._registrar_resultado(jugador_anterior.jugador_id, self.PENALIZACION_PERDEDOR, False)
            self._registrar_resultado(jugador_actual.jugador_id, self.APUESTA_BASE, True)
            
            resultado = f"{mensaje_dados}¡Correcto! Solo había {conteo_real} dados de {valor}. {jugador_anterior.nombre} pierde un dado."
        
        self._actualizar_dados_todos()
        self.ultima_apuesta = None
        
        if self._verificar_ganador():
            return True, f"{resultado}\n¡Juego terminado!"
        
        self._siguiente_turno()
        return True, resultado

    def _verificar_ganador(self):
        """Verifica si queda un solo jugador con dados y registra resultados finales"""
        jugadores_con_dados = [j for j in self.jugadores if len(self.dados_jugadores[j.jugador_id]) > 0]
        
        if len(jugadores_con_dados) == 1:
            ganador = jugadores_con_dados[0]
            premio = self.PREMIO_GANADOR * (len(self.jugadores) - 1)
            ganador.saldo += premio
            self._registrar_resultado(ganador.jugador_id, premio, True)
            
            # Registrar solo el resultado final para cada jugador
            for jugador in self.jugadores:
                total = abs(self.resultados_jugadores[jugador.jugador_id])
                if jugador.jugador_id == ganador.jugador_id:
                    jugador.agregar_jugada(f"Dado Mentiroso (Ganador)|GANO|{total}")
                else:
                    jugador.agregar_jugada(f"PERDIO|{total}")
            
            # Guardar historial
            resultado = {
                'ganador': ganador.jugador_id,
                'nombre': ganador.nombre,
                'premio': premio,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'jugadores': {
                    j.jugador_id: {
                        'nombre': j.nombre,
                        'dados_finales': len(self.dados_jugadores[j.jugador_id]),
                        'saldo_final': j.saldo
                    } for j in self.jugadores
                }
            }
            
            if hasattr(self, 'historial_service'):
                ultimo = self.historial_service.historiales[-1]
                ultimo.set_resultado(resultado)
                self.historial_service._guardar_historiales()
            
            return True
        
        return False

    def obtener_estado(self, jugador_id):
        """Devuelve el estado actual del juego para un jugador"""
        return {
            'jugadores': [{
                'jugador_id': j.jugador_id,
                'nombre': j.nombre,
                'dados_restantes': len(self.dados_jugadores[j.jugador_id]),
                'saldo': j.saldo
            } for j in self.jugadores],
            'turno_actual': self.jugadores[self.turno_actual].jugador_id,
            'ultima_apuesta': self.ultima_apuesta,
            'tus_dados': self.dados_jugadores.get(jugador_id, []),
        }
    
    def obtener_estrategia_recomendada(self, jugador_id: str) -> List[Tuple[Tuple[int, int], bool]]:
        """
        Obtiene una secuencia recomendada de apuestas usando backtracking.
        
        Args:
            jugador_id: ID del jugador para el que se calcula la estrategia
            
        Returns:
            Lista de tuplas ((cantidad, valor), es_segura) con la secuencia recomendada
        """
        if jugador_id not in self.dados_jugadores:
            return []
        
        dados_jugador = self.dados_jugadores[jugador_id]
        saldo_jugador = next(j.saldo for j in self.jugadores if j.jugador_id == jugador_id)
        
        # Generar apuestas posibles basadas en los dados y última apuesta
        apuestas_posibles = EstrategiaDadoMentiroso.generar_apuestas_posibles(
            dados_jugador, self.ultima_apuesta)
        
        if not apuestas_posibles:
            return []
        
        # Crear estrategia y encontrar mejor secuencia
        estrategia = EstrategiaDadoMentiroso(saldo_jugador, apuestas_posibles)
        mejor_secuencia, _ = estrategia.encontrar_mejor_estrategia(max_profundidad=4)
        
        return mejor_secuencia