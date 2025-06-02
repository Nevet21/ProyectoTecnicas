from typing import List, Tuple, Optional
import copy

class EstrategiaDadoMentiroso:
    def __init__(self, saldo_inicial: float, apuestas_posibles: List[Tuple[int, int]]):
        """
        Initializes the strategy with an initial balance and a list of possible bets.
        
        Args:
            saldo_inicial: Player's starting balance
            apuestas_posibles: List of tuples (quantity, value) representing possible bets
        """
        self.saldo_inicial = saldo_inicial
        self.apuestas_posibles = apuestas_posibles
        self.mejor_secuencia = []
        self.max_saldo = saldo_inicial
        
    def evaluar_apuesta(self, saldo_actual: float, apuesta: Tuple[int, int], es_segura: bool = False) -> float:
        """
        Evaluates the potential outcome of a bet based on the rules of Liar's Dice.
        
        Args:
            saldo_actual: Player's current balance
            apuesta: Tuple (quantity, value) representing the bet
            es_segura: Indicates whether it's a safe (challenge) bet
            
        Returns:
            The estimated new balance after the bet
        """
        cantidad, valor = apuesta
        
        # Estimated success probability (simplified example)
        # In a real scenario, this should be based on game statistics
        prob_exito = 0.5 if not es_segura else 0.3
        
        # Rewards and penalties based on the game's rules
        if es_segura:
            ganancia = 100  # WINNING_REWARD
            perdida = 60    # LOSING_PENALTY * 2
        else:
            ganancia = 50   # BASE_BET_REWARD
            perdida = 30    # LOSING_PENALTY
        
        # Calculate expected balance
        saldo_esperado = saldo_actual + (ganancia * prob_exito) - (perdida * (1 - prob_exito))
        
        # Ensure balance is not negative
        return max(0, saldo_esperado)
    
    def backtracking(self, saldo_actual: float, secuencia_actual: List[Tuple[Tuple[int, int], bool]], 
                    profundidad: int, max_profundidad: int = 5):
        """
        Backtracking algorithm to find the best sequence of bets.
        
        Args:
            saldo_actual: Current balance in this search branch
            secuencia_actual: Sequence of bets made so far
            profundidad: Current depth in the decision tree
            max_profundidad: Maximum depth to explore
        """
        # Termination condition
        if profundidad >= max_profundidad or saldo_actual <= 0:
            if saldo_actual > self.max_saldo:
                self.max_saldo = saldo_actual
                self.mejor_secuencia = copy.deepcopy(secuencia_actual)
            return
        
        # Explore all possible bets
        for apuesta in self.apuestas_posibles:
            # Try normal bet
            nuevo_saldo = self.evaluar_apuesta(saldo_actual, apuesta, es_segura=False)
            secuencia_actual.append((apuesta, False))
            self.backtracking(nuevo_saldo, secuencia_actual, profundidad + 1, max_profundidad)
            secuencia_actual.pop()
            
            # Try safe bet (only if it makes sense in the game context)
            if profundidad < max_profundidad - 1:  # Safe bets are riskier, explore fewer
                nuevo_saldo_segura = self.evaluar_apuesta(saldo_actual, apuesta, es_segura=True)
                secuencia_actual.append((apuesta, True))
                self.backtracking(nuevo_saldo_segura, secuencia_actual, profundidad + 1, max_profundidad)
                secuencia_actual.pop()
    
    def encontrar_mejor_estrategia(self, max_profundidad: int = 5) -> Tuple[List[Tuple[Tuple[int, int], bool]], float]:
        """
        Finds the best sequence of bets.
        
        Args:
            max_profundidad: Maximum depth to explore in the decision tree
            
        Returns:
            Tuple containing (best_sequence, estimated_final_balance)
        """
        self.mejor_secuencia = []
        self.max_saldo = self.saldo_inicial
        self.backtracking(self.saldo_inicial, [], 0, max_profundidad)
        return self.mejor_secuencia, self.max_saldo

    @staticmethod
    def generar_apuestas_posibles(dados_actuales: List[int], ultima_apuesta: Optional[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
        """
        Generates possible bets based on the player's dice and the last bet.
        
        Args:
            dados_actuales: List of the player's dice values
            ultima_apuesta: Last bet made (quantity, value) or None
            
        Returns:
            List of possible bets (quantity, value)
        """
        apuestas_posibles = []
        conteo_dados = {valor: dados_actuales.count(valor) for valor in set(dados_actuales)}
        
        # If there is no last bet, the player can start with any value
        if not ultima_apuesta:
            for valor in range(1, 7):
                for cantidad in range(1, len(dados_actuales) + 2):  # +2 allows some bluffing
                    apuestas_posibles.append((cantidad, valor))
        else:
            ultima_cant, ultimo_val = ultima_apuesta
            # Bets increasing the quantity
            for cantidad in range(ultima_cant + 1, len(dados_actuales) + 5):  # +5 allows bluffing margin
                apuestas_posibles.append((cantidad, ultimo_val))
            
            # Bets with same quantity but higher value
            for valor in range(ultimo_val + 1, 7):
                apuestas_posibles.append((ultima_cant, valor))
        
        return apuestas_posibles
