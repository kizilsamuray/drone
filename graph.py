import heapq
from typing import Dict, List, Set, Tuple

class Graph:
    """
    Graf sınıfı, dronun hareket edeceği ağı temsil eder.
    Her düğüm bir konumu, her kenar ise iki konum arasındaki bağlantıyı temsil eder.
    """
    def __init__(self, num_nodes: int):
        """
        Args:
            num_nodes (int): Graf içindeki toplam düğüm sayısı
        """
        self.num_nodes = num_nodes
        self.graph: Dict[int, List[int]] = {i: [] for i in range(num_nodes)}
        # Her kenar sadece hedef düğümü saklar
        
    def add_edge(self, from_node: int, to_node: int):
        """
        İki düğüm arasına bağlantı ekler.
        
        Args:
            from_node (int): Başlangıç düğümü
            to_node (int): Bitiş düğümü
        """
        self.graph[from_node].append(to_node)
        self.graph[to_node].append(from_node)  # Yönsüz graf
        
    def dijkstra(self, start: int, end: int) -> List[int]:
        """
        Dijkstra algoritması ile en kısa yolu bulur.
        
        Args:
            start (int): Başlangıç düğümü
            end (int): Bitiş düğümü
            
        Returns:
            List[int]: Bulunan yol
        """
        distances = {i: float('infinity') for i in range(self.num_nodes)}
        distances[start] = 0
        previous = {i: None for i in range(self.num_nodes)}
        
        pq = [(0, start)]  # Öncelik kuyruğu
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node == end:
                break
                
            if current_distance > distances[current_node]:
                continue
                
            for neighbor in self.graph[current_node]:
                new_distance = distances[current_node] + 1  # Her kenar 1 birim uzunluğunda
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
        
        # Yolu geri oluştur
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return path
    
    def get_alternative_paths(self, start: int, end: int, num_paths: int = 2) -> List[List[int]]:
        """
        Başlangıç ve bitiş noktaları arasında alternatif yollar bulur.
        
        Args:
            start (int): Başlangıç düğümü
            end (int): Bitiş düğümü
            num_paths (int): Bulunacak alternatif yol sayısı
            
        Returns:
            List[List[int]]: Alternatif yollar listesi
        """
        paths = []
        visited_edges = set()
        
        for _ in range(num_paths):
            path = self.dijkstra(start, end)
            paths.append(path)
            
            # Bu yoldaki kenarları işaretle
            for i in range(len(path) - 1):
                visited_edges.add((path[i], path[i + 1]))
                visited_edges.add((path[i + 1], path[i]))
        
        return paths
