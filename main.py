from graph import Graph
from hamming import HammingCode
from montecarlo import MonteCarloSimulation
from minimax import MinimaxRouteSelector
from tasks import TaskQueue, TaskStatus
import time
import random

class RescueDroneSimulation:
    """
    Kurtarma Dronu Simülasyonu ana sınıfı.
    Tüm bileşenleri bir araya getirir ve simülasyonu yönetir.
    """
    def __init__(self, num_nodes: int = 10):
        """python main.py
        Args:
            num_nodes (int): Simülasyon alanındaki düğüm sayısı
        """
        self.graph = Graph(num_nodes)
        self.monte_carlo = MonteCarloSimulation(num_nodes)
        self.route_selector = MinimaxRouteSelector()
        self.task_queue = TaskQueue()
        self.hamming = HammingCode()
        
        # Grafı başlat
        self._initialize_graph()
        
    def _initialize_graph(self):
        """Grafı rastgele bağlantılarla başlatır"""
        for i in range(self.graph.num_nodes):
            for j in range(i + 1, self.graph.num_nodes):
                if random.random() < 0.3:  # %30 olasılıkla bağlantı ekle
                    self.graph.add_edge(i, j)
                    
    def add_rescue_task(self, target_node: int, priority: int, description: str):
        """
        Yeni bir kurtarma görevi ekler.
        
        Args:
            target_node (int): Hedef düğüm
            priority (int): Görev önceliği
            description (str): Görev açıklaması
        """
        self.task_queue.add_task(target_node, priority, description)
        
    def simulate_rescue_mission(self):
        """
        Kurtarma görevini simüle eder.
        Dron, görevleri öncelik sırasına göre gerçekleştirir.
        """
        print("Kurtarma görevi başlıyor...")
        
        while True:
            # Sonraki görevi al
            task = self.task_queue.get_next_task()
            if not task:
                print("Tüm görevler tamamlandı!")
                break
                
            print(f"\nGörev #{task.id}: {task.description}")
            print(f"Hedef: Düğüm {task.target_node}")
            
            # Görevi başlat
            self.task_queue.update_task_status(task.id, TaskStatus.IN_PROGRESS)
            
            # Alternatif rotaları bul
            paths = self.graph.get_alternative_paths(0, task.target_node)
            
            # En iyi rotayı seç
            best_path = self.route_selector.select_best_route(paths)
            
            print(f"Seçilen rota: {best_path}")
            
            # Rotayı takip et
            for i in range(len(best_path) - 1):
                current = best_path[i]
                next_node = best_path[i + 1]
                
                # Konum bilgisini ilet
                location_data = f"Konum: {current} -> {next_node}"
                encoded_data = self.hamming.encode(location_data)
                
                # Hata simülasyonu
                if random.random() < 0.2:  # %20 hata olasılığı
                    encoded_data = self.hamming.simulate_error(encoded_data)
                    print("Konum verisi bozuldu!")
                
                # Hatayı düzelt
                decoded_data = self.hamming.decode(encoded_data)
                print(f"İletilen veri: {decoded_data}")
                
                # Engel kontrolü
                if self.monte_carlo.is_path_blocked(current, next_node):
                    print(f"Uyarı: {current} -> {next_node} arası engelli!")
                    delay = self.monte_carlo.get_delay_factor(current, next_node)
                    time.sleep(delay)
                    
            # Görevi tamamla
            self.task_queue.update_task_status(task.id, TaskStatus.COMPLETED)
            print(f"Görev #{task.id} tamamlandı!")
            
        # İstatistikleri göster
        stats = self.task_queue.get_task_stats()
        print("\nGörev İstatistikleri:")
        for status, count in stats.items():
            print(f"{status}: {count}")

if __name__ == "__main__":
    # Simülasyonu başlat
    sim = RescueDroneSimulation()
    
    # Örnek görevler ekle
    sim.add_rescue_task(3, 1, "Acil durum: Yaralı kurtarma")
    sim.add_rescue_task(7, 2, "Malzeme teslimatı")
    sim.add_rescue_task(5, 3, "Bölge keşfi")
    
    # Simülasyonu çalıştır
    sim.simulate_rescue_mission()
