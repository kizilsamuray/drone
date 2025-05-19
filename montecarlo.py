import random
from typing import List, Tuple, Dict

class MonteCarloSimulation:
    """
    Monte Carlo Simülasyon sınıfı, ortamdaki rastgele engelleri ve gecikmeleri simüle eder.
    Dronun karşılaşabileceği çevresel faktörleri modellemek için kullanılır.
    """
    def __init__(self, num_nodes: int):
        """
        Args:
            num_nodes (int): Simülasyon alanındaki toplam düğüm sayısı
        """
        self.num_nodes = num_nodes
        self.obstacles: Dict[Tuple[int, int], float] = {}  # (düğüm1, düğüm2) -> engel_olasılığı
        self.delays: Dict[Tuple[int, int], float] = {}     # (düğüm1, düğüm2) -> gecikme_faktörü
        
    def generate_obstacles(self, probability: float = 0.3):
        """
        Düğümler arasında rastgele engeller oluşturur.
        
        Args:
            probability (float): Engel oluşturma olasılığı (0-1 arası)
        """
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < probability:
                    self.obstacles[(i, j)] = random.uniform(0.1, 1.0)
                    self.obstacles[(j, i)] = self.obstacles[(i, j)]
                    
    def generate_delays(self, max_delay: float = 2.0):
        """
        Düğümler arasında rastgele gecikmeler oluşturur.
        
        Args:
            max_delay (float): Maksimum gecikme faktörü
        """
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                if random.random() < 0.4:  # %40 gecikme olasılığı
                    delay = random.uniform(1.0, max_delay)
                    self.delays[(i, j)] = delay
                    self.delays[(j, i)] = delay
                    
    def is_path_blocked(self, from_node: int, to_node: int) -> bool:
        """
        İki düğüm arasındaki yolun engelli olup olmadığını kontrol eder.
        
        Args:
            from_node (int): Başlangıç düğümü
            to_node (int): Bitiş düğümü
            
        Returns:
            bool: Yol engelli ise True, değilse False
        """
        edge = (min(from_node, to_node), max(from_node, to_node))
        if edge in self.obstacles:
            return random.random() < self.obstacles[edge]
        return False
        
    def get_delay_factor(self, from_node: int, to_node: int) -> float:
        """
        İki düğüm arasındaki yolun gecikme faktörünü döndürür.
        
        Args:
            from_node (int): Başlangıç düğümü
            to_node (int): Bitiş düğümü
            
        Returns:
            float: Gecikme faktörü (1.0 = normal hız)
        """
        edge = (min(from_node, to_node), max(from_node, to_node))
        return self.delays.get(edge, 1.0)
        
    def simulate_environment(self, num_simulations: int = 1000) -> Dict[str, float]:
        """
        Monte Carlo simülasyonu çalıştırarak ortamı analiz eder.
        
        Args:
            num_simulations (int): Simülasyon sayısı
            
        Returns:
            Dict[str, float]: Simülasyon sonuçları
                - avg_obstacles: Ortalama engel sayısı
                - avg_delays: Ortalama gecikme faktörü
                - max_delay: Maksimum gecikme faktörü
        """
        results = {
            'avg_obstacles': 0,
            'avg_delays': 0,
            'max_delay': 0
        }
        
        for _ in range(num_simulations):
            self.generate_obstacles()
            self.generate_delays()
            
            results['avg_obstacles'] += len(self.obstacles) / num_simulations
            results['avg_delays'] += sum(self.delays.values()) / num_simulations
            results['max_delay'] = max(results['max_delay'], max(self.delays.values()) if self.delays else 0)
            
        return results
