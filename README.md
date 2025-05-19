# Akıllı Kurtarma Dronu Simülasyonu

Bu proje, doğal afet bölgelerinde görev yapan bir kurtarma dronunun simülasyonunu içerir. Dron, birden fazla hedefe en uygun rotayı izleyerek ulaşır ve ortamdan kaynaklı bilgi bozulmalarını tespit edip düzeltir.

## Özellikler

- Dijkstra algoritması ile en kısa yol hesaplama
- Hamming kodu ile hata tespiti ve düzeltme
- Monte Carlo simülasyonu ile rastgele engel ve gecikme modelleme
- Minimax algoritması ile stratejik rota seçimi
- Öncelikli görev yönetimi

## Proje Yapısı

```
/rescue_drone_sim/
│
├── main.py               # Ana simülasyon dosyası
├── graph.py              # Graf yapısı ve yol hesaplamaları
├── hamming.py            # Hata tespiti ve düzeltme
├── montecarlo.py         # Rastgele engel ve gecikme simülasyonu
├── minimax.py            # Stratejik rota seçimi
├── tasks.py              # Görev yönetim sistemi
└── README.md             # Açıklama ve kullanım
```

## Kullanım

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Simülasyonu çalıştırın:
```bash
python main.py
```

## Simülasyon Senaryosu

1. Afet bölgesi 10 düğümlü bir graf olarak tanımlanır
2. Dron başlangıç noktasından çıkış yapar
3. Görevler öncelik sırasına göre işlenir
4. Her görev için:
   - Dijkstra ile en kısa yol hesaplanır
   - Monte Carlo ile engeller simüle edilir
   - Konum verileri Hamming kodu ile korunur
   - Minimax ile en uygun rota seçilir

## Test Senaryoları

1. 3 hedef nokta → Dron sırayla hepsine uğrar
2. 2 rota sunulur: biri kısa ama engelli, biri uzun ama temiz
3. Konum verisi rastgele bozulur → Hamming ile düzeltilir
4. Görev listesi sonunda sıralı şekilde gösterilir

