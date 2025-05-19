class HammingCode:
    """
    Hamming Kod sınıfı, veri iletiminde hata tespiti ve düzeltmesi için kullanılır.
    Dronun konum bilgilerinin güvenli iletimini sağlar.
    """
    @staticmethod
    def encode(data: str) -> str:
        """
        Veriyi Hamming kod ile kodlar.
        
        Args:
            data (str): Kodlanacak veri
            
        Returns:
            str: Hamming kod ile kodlanmış veri
        """
        # String'i binary'e çevir
        binary = ''.join(format(ord(c), '08b') for c in data)
        
        # Gerekli parite biti sayısını hesapla
        m = len(binary)
        r = 1
        while 2**r < m + r + 1:
            r += 1
            
        # Parite bitleriyle birlikte kodlanmış mesajı oluştur
        encoded = ['0'] * (m + r)
        j = 0
        for i in range(1, m + r + 1):
            if i & (i - 1) == 0:  # 2'nin kuvveti
                continue
            encoded[i-1] = binary[j]
            j += 1
            
        # Parite bitlerini hesapla
        for i in range(r):
            pos = 2**i
            count = 0
            for j in range(pos, len(encoded) + 1):
                if j & pos:
                    if encoded[j-1] == '1':
                        count += 1
            encoded[pos-1] = '1' if count % 2 else '0'
            
        return ''.join(encoded)
    
    @staticmethod
    def decode(encoded: str) -> str:
        """
        Hamming kod ile kodlanmış veriyi çözer ve hataları düzeltir.
        
        Args:
            encoded (str): Kodlanmış veri
            
        Returns:
            str: Çözülmüş ve düzeltilmiş veri
        """
        # Parite biti sayısını hesapla
        r = 1
        while 2**r < len(encoded) + 1:
            r += 1
            
        # Hataları kontrol et
        error_pos = 0
        for i in range(r):
            pos = 2**i
            count = 0
            for j in range(pos, len(encoded) + 1):
                if j & pos:
                    if encoded[j-1] == '1':
                        count += 1
            if count % 2:
                error_pos += pos
                
        # Hatayı düzelt
        if error_pos:
            encoded = list(encoded)
            encoded[error_pos-1] = '1' if encoded[error_pos-1] == '0' else '0'
            encoded = ''.join(encoded)
            
        # Parite bitlerini kaldır ve string'e çevir
        result = ''
        j = 0
        for i in range(1, len(encoded) + 1):
            if i & (i - 1) == 0:  # 2'nin kuvveti
                continue
            result += encoded[i-1]
            j += 1
            
        # Binary'i string'e çevir
        return ''.join(chr(int(result[i:i+8], 2)) for i in range(0, len(result), 8))
    
    @staticmethod
    def simulate_error(encoded: str, num_errors: int = 1) -> str:
        """
        Kodlanmış veride rastgele hatalar oluşturur (test için).
        
        Args:
            encoded (str): Kodlanmış veri
            num_errors (int): Oluşturulacak hata sayısı
            
        Returns:
            str: Hatalı kodlanmış veri
        """
        import random
        encoded = list(encoded)
        for _ in range(num_errors):
            pos = random.randint(0, len(encoded) - 1)
            encoded[pos] = '1' if encoded[pos] == '0' else '0'
        return ''.join(encoded)
