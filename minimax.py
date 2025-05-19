from typing import List, Tuple, Dict
import math

class MinimaxRouteSelector:
    """
    Minimax Rota Seçici sınıfı, dronun en uygun rotayı seçmesi için kullanılır.
    Yolları değerlendirerek en iyi rotayı belirler.
    """
    def __init__(self, max_depth: int = 3):
        """
        Args:
            max_depth (int): Minimax algoritmasının maksimum derinliği
        """
        self.max_depth = max_depth
        
    def evaluate_route(self, path: List[int]) -> float:
        """
        Bir rotayı değerlendirir.
        
        Args:
            path (List[int]): Rota düğümleri
            
        Returns:
            float: Rota değerlendirme puanı (0-1 arası)
        """
        # Yol uzunluğuna göre değerlendirme
        return 1.0 / (1.0 + len(path))
        
    def minimax(self, paths: List[List[int]], depth: int, 
                alpha: float, beta: float, maximizing: bool) -> Tuple[float, int]:
        """
        Minimax algoritması ile en iyi rotayı seçer (alpha-beta budama ile).
        
        Args:
            paths: Değerlendirilecek rotalar listesi
            depth: Arama derinliği
            alpha: Alpha değeri (alpha-beta budama için)
            beta: Beta değeri (alpha-beta budama için)
            maximizing: Maksimizasyon modunda mı?
            
        Returns:
            Tuple[float, int]: (en iyi değerlendirme puanı, en iyi rota indeksi)
        """
        if depth == 0 or not paths:
            return (0, -1)
            
        if maximizing:
            max_eval = float('-inf')
            best_path_idx = -1
            
            for i, path in enumerate(paths):
                eval = self.evaluate_route(path)
                if eval > max_eval:
                    max_eval = eval
                    best_path_idx = i
                    
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                    
            return (max_eval, best_path_idx)
        else:
            min_eval = float('inf')
            best_path_idx = -1
            
            for i, path in enumerate(paths):
                eval = self.evaluate_route(path)
                if eval < min_eval:
                    min_eval = eval
                    best_path_idx = i
                    
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                    
            return (min_eval, best_path_idx)
            
    def select_best_route(self, paths: List[List[int]]) -> List[int]:
        """
        Minimax algoritması kullanarak en iyi rotayı seçer.
        
        Args:
            paths: Değerlendirilecek rotalar listesi
            
        Returns:
            List[int]: Seçilen en iyi rota
        """
        if not paths:
            return []
            
        # Tüm rotaları değerlendir
        evaluated_paths = []
        for path in paths:
            score = self.evaluate_route(path)
            evaluated_paths.append((path, score))
            
        # Rotaları puana göre sırala
        evaluated_paths.sort(key=lambda x: x[1], reverse=True)
        
        # Minimax ile en iyi rotayı seç
        _, best_idx = self.minimax(paths, self.max_depth, float('-inf'), float('inf'), True)
        
        return paths[best_idx]
