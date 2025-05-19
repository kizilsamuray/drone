from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

class TaskStatus(Enum):
    """Görev durumlarını temsil eden enum sınıfı"""
    PENDING = "beklemede"
    IN_PROGRESS = "devam_ediyor"
    COMPLETED = "tamamlandı"
    FAILED = "başarısız"

@dataclass
class Task:
    """Görev sınıfı, dronun yapması gereken işlemleri temsil eder"""
    id: int
    target_node: int
    priority: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = time.time()
    completed_at: Optional[float] = None

class TaskQueue:
    """
    Görev Kuyruğu sınıfı, dronun yapması gereken görevleri yönetir.
    Öncelikli görevler önce işlenir.
    """
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1
        
    def add_task(self, target_node: int, priority: int, description: str) -> Task:
        """
        Yeni bir görev ekler.
        
        Args:
            target_node (int): Hedef düğüm
            priority (int): Görev önceliği (düşük sayı = yüksek öncelik)
            description (str): Görev açıklaması
            
        Returns:
            Task: Oluşturulan görev
        """
        task = Task(
            id=self.next_id,
            target_node=target_node,
            priority=priority,
            description=description
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
        
    def get_next_task(self) -> Optional[Task]:
        """
        Önceliği en yüksek olan bekleyen görevi döndürür.
        
        Returns:
            Optional[Task]: Bir sonraki görev veya None
        """
        pending_tasks = [
            task for task in self.tasks.values()
            if task.status == TaskStatus.PENDING
        ]
        
        if not pending_tasks:
            return None
            
        return min(pending_tasks, key=lambda t: t.priority)
        
    def update_task_status(self, task_id: int, status: TaskStatus) -> bool:
        """
        Görev durumunu günceller.
        
        Args:
            task_id (int): Görev ID'si
            status (TaskStatus): Yeni durum
            
        Returns:
            bool: Güncelleme başarılı ise True
        """
        if task_id not in self.tasks:
            return False
            
        task = self.tasks[task_id]
        task.status = status
        
        if status == TaskStatus.COMPLETED:
            task.completed_at = time.time()
            
        return True
        
    def get_task_stats(self) -> Dict[str, int]:
        """
        Görev istatistiklerini döndürür.
        
        Returns:
            Dict[str, int]: Durumlara göre görev sayıları
        """
        stats = {status.value: 0 for status in TaskStatus}
        
        for task in self.tasks.values():
            stats[task.status.value] += 1
            
        return stats
