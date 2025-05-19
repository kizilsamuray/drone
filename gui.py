import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                           QSpinBox, QComboBox, QTableWidget, QTableWidgetItem,
                           QFrame, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from main import RescueDroneSimulation
from tasks import TaskStatus
import random
import time

class DroneSimulationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation = RescueDroneSimulation()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Kurtarma Dronu Simülasyonu')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
            QSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Üst panel - Kontroller
        control_group = QGroupBox("Görev Kontrol Paneli")
        control_layout = QGridLayout()
        control_group.setLayout(control_layout)
        
        # Hedef düğüm seçimi
        target_label = QLabel("Hedef Düğüm:")
        self.target_spin = QSpinBox()
        self.target_spin.setRange(0, 9)
        self.target_spin.setFixedWidth(100)
        
        # Öncelik seçimi
        priority_label = QLabel("Öncelik:")
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Yüksek", "Orta", "Düşük"])
        self.priority_combo.setFixedWidth(150)
        
        # Görev açıklaması
        desc_label = QLabel("Görev Açıklaması:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(50)
        
        # Görev ekle butonu
        add_task_btn = QPushButton("Görev Ekle")
        add_task_btn.setFixedWidth(150)
        add_task_btn.clicked.connect(self.add_task)
        
        # Kontrolleri grid'e ekle
        control_layout.addWidget(target_label, 0, 0)
        control_layout.addWidget(self.target_spin, 0, 1)
        control_layout.addWidget(priority_label, 0, 2)
        control_layout.addWidget(self.priority_combo, 0, 3)
        control_layout.addWidget(desc_label, 1, 0)
        control_layout.addWidget(self.desc_edit, 1, 1, 1, 3)
        control_layout.addWidget(add_task_btn, 1, 4)
        
        # Simülasyon kontrol butonları
        button_group = QGroupBox("Simülasyon Kontrolleri")
        button_layout = QHBoxLayout()
        button_group.setLayout(button_layout)
        
        start_btn = QPushButton("▶ Başlat")
        start_btn.setFixedWidth(120)
        start_btn.clicked.connect(self.start_simulation)
        
        pause_btn = QPushButton("⏸ Duraklat")
        pause_btn.setFixedWidth(120)
        pause_btn.clicked.connect(self.pause_simulation)
        
        reset_btn = QPushButton("⟳ Sıfırla")
        reset_btn.setFixedWidth(120)
        reset_btn.clicked.connect(self.reset_simulation)
        
        button_layout.addWidget(start_btn)
        button_layout.addWidget(pause_btn)
        button_layout.addWidget(reset_btn)
        
        # Alt panel - Görev listesi ve log
        bottom_group = QGroupBox("Simülasyon Durumu")
        bottom_layout = QHBoxLayout()
        bottom_group.setLayout(bottom_layout)
        
        # Görev tablosu
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["Görev ID", "Hedef", "Öncelik", "Durum"])
        self.task_table.setMinimumWidth(500)
        self.task_table.horizontalHeader().setStretchLastSection(True)
        
        # Log alanı
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        # Alt panel'e widget'ları ekle
        bottom_layout.addWidget(self.task_table)
        bottom_layout.addWidget(self.log_text)
        
        # Ana layout'a grupları ekle
        layout.addWidget(control_group)
        layout.addWidget(button_group)
        layout.addWidget(bottom_group)
        
        # Timer için değişkenler
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.is_running = False
        
        # Başlangıç mesajı
        self.log_text.append("Simülasyon hazır. Görev ekleyip başlatabilirsiniz.")
        
    def add_task(self):
        target = self.target_spin.value()
        priority_map = {"Yüksek": 1, "Orta": 2, "Düşük": 3}
        priority = priority_map[self.priority_combo.currentText()]
        description = self.desc_edit.toPlainText()
        
        if description:
            task = self.simulation.add_rescue_task(target, priority, description)
            self.update_task_table()
            self.log_text.append(f"✅ Yeni görev eklendi: {description}")
            self.desc_edit.clear()
            
    def update_task_table(self):
        self.task_table.setRowCount(0)
        for task_id, task in self.simulation.task_queue.tasks.items():
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)
            
            # Görev ID
            id_item = QTableWidgetItem(str(task.id))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.task_table.setItem(row, 0, id_item)
            
            # Hedef
            target_item = QTableWidgetItem(str(task.target_node))
            target_item.setTextAlignment(Qt.AlignCenter)
            self.task_table.setItem(row, 1, target_item)
            
            # Öncelik
            priority_item = QTableWidgetItem(str(task.priority))
            priority_item.setTextAlignment(Qt.AlignCenter)
            self.task_table.setItem(row, 2, priority_item)
            
            # Durum
            status_text = task.status.name if isinstance(task.status, TaskStatus) else str(task.status)
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            if status_text == "COMPLETED":
                status_item.setBackground(QColor("#90EE90"))  # Açık yeşil
            elif status_text == "IN_PROGRESS":
                status_item.setBackground(QColor("#FFD700"))  # Altın sarısı
            elif status_text == "ERROR":
                status_item.setBackground(QColor("#FFB6C1"))  # Açık kırmızı
            self.task_table.setItem(row, 3, status_item)
            
    def start_simulation(self):
        if not self.is_running:
            try:
                self.is_running = True
                self.timer.start(1000)  # Her saniye güncelle
                self.log_text.append("Kurtarma görevi başlıyor...")
                
                # Simülasyonu başlat
                task = self.simulation.task_queue.get_next_task()
                if task:
                    self.simulation.task_queue.update_task_status(task.id, TaskStatus.IN_PROGRESS)
                    self.update_task_table()
            except Exception as e:
                self.is_running = False
                self.timer.stop()
                self.log_text.append(f"Hata oluştu: {str(e)}")
                self.log_text.append("Simülasyon durduruldu.")
            
    def pause_simulation(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.log_text.append("⏸ Simülasyon duraklatıldı...")
            
    def reset_simulation(self):
        self.simulation = RescueDroneSimulation()
        self.is_running = False
        self.timer.stop()
        self.update_task_table()
        self.log_text.clear()
        self.log_text.append("🔄 Simülasyon sıfırlandı...")
        
    def update_simulation(self):
        if self.is_running:
            try:
                # Mevcut görevi tamamla
                for task_id, task in self.simulation.task_queue.tasks.items():
                    if task.status == TaskStatus.IN_PROGRESS:
                        try:
                            self.log_text.append(f"\nGörev #{task.id}: {task.description}")
                            self.log_text.append(f"Hedef: Düğüm {task.target_node}")
                            
                            # Alternatif rotaları bul
                            paths = self.simulation.graph.get_alternative_paths(0, task.target_node)
                            
                            # En iyi rotayı seç
                            best_path = self.simulation.route_selector.select_best_route(paths)
                            self.log_text.append(f"Seçilen rota: {best_path}")
                            
                            # Rotayı takip et
                            for i in range(len(best_path) - 1):
                                current = best_path[i]
                                next_node = best_path[i + 1]
                                
                                # Konum bilgisini ilet
                                location_data = f"Konum: {current} -> {next_node}"
                                encoded_data = self.simulation.hamming.encode(location_data)
                                
                                # Hata simülasyonu
                                if random.random() < 0.2:  # %20 hata olasılığı
                                    encoded_data = self.simulation.hamming.simulate_error(encoded_data)
                                    self.log_text.append("Konum verisi bozuldu!")
                                
                                # Hatayı düzelt
                                decoded_data = self.simulation.hamming.decode(encoded_data)
                                self.log_text.append(f"İletilen veri: {decoded_data}")
                                
                                # Engel kontrolü
                                if self.simulation.monte_carlo.is_path_blocked(current, next_node):
                                    self.log_text.append(f"Uyarı: {current} -> {next_node} arası engelli!")
                                    delay = self.simulation.monte_carlo.get_delay_factor(current, next_node)
                                    time.sleep(delay)
                            
                            # Görevi tamamla
                            self.simulation.task_queue.update_task_status(task_id, TaskStatus.COMPLETED)
                            self.log_text.append(f"Görev #{task.id} tamamlandı!")
                            
                            # İstatistikleri göster
                            stats = self.simulation.task_queue.get_task_stats()
                            self.log_text.append("\nGörev İstatistikleri:")
                            for status, count in stats.items():
                                self.log_text.append(f"{status}: {count}")
                            
                        except Exception as e:
                            self.log_text.append(f"Görev çalıştırılırken hata oluştu: {str(e)}")
                            self.simulation.task_queue.update_task_status(task_id, TaskStatus.ERROR)
                        break
                
                # Yeni görev başlat
                task = self.simulation.task_queue.get_next_task()
                if task:
                    self.simulation.task_queue.update_task_status(task.id, TaskStatus.IN_PROGRESS)
                else:
                    self.log_text.append("\nTüm görevler tamamlandı!")
                    self.is_running = False
                    self.timer.stop()
                
                self.update_task_table()
            except Exception as e:
                self.is_running = False
                self.timer.stop()
                self.log_text.append(f"Beklenmeyen bir hata oluştu: {str(e)}")
                self.log_text.append("Simülasyon durduruldu.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DroneSimulationGUI()
    gui.show()
    sys.exit(app.exec_()) 