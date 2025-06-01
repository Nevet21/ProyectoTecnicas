from typing import List, Tuple, Optional
import copy

class EstrategiaDadoMentiroso:
    def __init__(self, saldo_inicial: float, apuestas_posibles: List[Tuple[int, int]]):
        """
        Inicializa la estrategia con saldo inicial y posibles apuestas.
        
        Args:
            saldo_inicial: Saldo inicial del jugador
            apuestas_posibles: Lista de tuplas (cantidad, valor) representando apuestas posibles
        """
        self.saldo_inicial = saldo_inicial
        self.apuestas_posibles = apuestas_posibles
        self.mejor_secuencia = []
        self.max_saldo = saldo_inicial
        
    def evaluar_apuesta(self, saldo_actual: float, apuesta: Tuple[int, int], es_segura: bool = False) -> float:
        """
        Evalúa el resultado potencial de una apuesta basado en las reglas del Dado Mentiroso.
        
        Args:
            saldo_actual: Saldo actual del jugador
            apuesta: Tupla (cantidad, valor) representando la apuesta
            es_segura: Indica si es una apuesta segura
            
        Returns:
            El nuevo saldo estimado después de la apuesta
        """
        cantidad, valor = apuesta
        
        # Probabilidad estimada de éxito (simplificada para el ejemplo)
        # En un caso real, esto debería basarse en estadísticas del juego
        prob_exito = 0.5 if not es_segura else 0.3
        
        # Recompensas y penalizaciones basadas en las reglas del Dado Mentiroso
        if es_segura:
            ganancia = 100  # PREMIO_GANADOR
            perdida = 60    # PENALIZACION_PERDEDOR * 2
        else:
            ganancia = 50    # APUESTA_BASE
            perdida = 30     # PENALIZACION_PERDEDOR
        
        # Calculamos el saldo esperado
        saldo_esperado = saldo_actual + (ganancia * prob_exito) - (perdida * (1 - prob_exito))
        
        # Aseguramos que el saldo no sea negativo
        return max(0, saldo_esperado)
    
    def backtracking(self, saldo_actual: float, secuencia_actual: List[Tuple[Tuple[int, int], bool]], 
                    profundidad: int, max_profundidad: int = 5):
        """
        Algoritmo de backtracking para encontrar la mejor secuencia de apuestas.
        
        Args:
            saldo_actual: Saldo actual en esta rama de búsqueda
            secuencia_actual: Secuencia de apuestas hasta este punto
            profundidad: Profundidad actual en el árbol de búsqueda
            max_profundidad: Profundidad máxima a explorar
        """
        # Condición de terminación
        if profundidad >= max_profundidad or saldo_actual <= 0:
            if saldo_actual > self.max_saldo:
                self.max_saldo = saldo_actual
                self.mejor_secuencia = copy.deepcopy(secuencia_actual)
            return
        
        # Explorar todas las apuestas posibles
        for apuesta in self.apuestas_posibles:
            # Probar apuesta normal
            nuevo_saldo = self.evaluar_apuesta(saldo_actual, apuesta, es_segura=False)
            secuencia_actual.append((apuesta, False))
            self.backtracking(nuevo_saldo, secuencia_actual, profundidad + 1, max_profundidad)
            secuencia_actual.pop()
            
            # Probar apuesta segura (solo si tiene sentido en el contexto del juego)
            if profundidad < max_profundidad - 1:  # Las apuestas seguras suelen ser más arriesgadas
                nuevo_saldo_segura = self.evaluar_apuesta(saldo_actual, apuesta, es_segura=True)
                secuencia_actual.append((apuesta, True))
                self.backtracking(nuevo_saldo_segura, secuencia_actual, profundidad + 1, max_profundidad)
                secuencia_actual.pop()
    
    def encontrar_mejor_estrategia(self, max_profundidad: int = 5) -> Tuple[List[Tuple[Tuple[int, int], bool]], float]:
        """
        Encuentra la mejor secuencia de apuestas.
        
        Args:
            max_profundidad: Profundidad máxima a explorar en el árbol de decisiones
            
        Returns:
            Tupla con (mejor_secuencia, saldo_final_estimado)
        """
        self.mejor_secuencia = []
        self.max_saldo = self.saldo_inicial
        self.backtracking(self.saldo_inicial, [], 0, max_profundidad)
        return self.mejor_secuencia, self.max_saldo

    @staticmethod
    def generar_apuestas_posibles(dados_actuales: List[int], ultima_apuesta: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        """
        Genera apuestas posibles basadas en los dados actuales y la última apuesta.
        
        Args:
            dados_actuales: Lista de valores de dados del jugador
            ultima_apuesta: Última apuesta realizada (cantidad, valor) o None
            
        Returns:
            Lista de apuestas posibles (cantidad, valor)
        """
        apuestas_posibles = []
        conteo_dados = {valor: dados_actuales.count(valor) for valor in set(dados_actuales)}
        
        # Si no hay última apuesta, podemos empezar con cualquier valor
        if not ultima_apuesta:
            for valor in range(1, 7):
                for cantidad in range(1, len(dados_actuales) + 2):  # +2 para permitir algo de bluff
                    apuestas_posibles.append((cantidad, valor))
        else:
            ultima_cant, ultimo_val = ultima_apuesta
            # Apuestas que aumentan la cantidad
            for cantidad in range(ultima_cant + 1, len(dados_actuales) + 5):  # +5 para permitir bluff
                apuestas_posibles.append((cantidad, ultimo_val))
            
            # Apuestas que mantienen cantidad pero aumentan valor
            for valor in range(ultimo_val + 1, 7):
                apuestas_posibles.append((ultima_cant, valor))
        
        return apuestas_posibles