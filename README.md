## Özellikler
- **Anlık Hareket Algılama:** Görüntü işleme teknikleri (Gaussian Blur, Thresholding ve Dilatasyon) ile arka plan farkı analizi.
- **Otomatik Kayıt Sistemi:** Hareket algılandığı an 1 dakikalık video kaydı başlatma.
- **Güvenli Telegram Entegrasyonu:** Hareket anında anlık metin bildirimi ve kayıt bittiğinde video dosyasının şifreli aktarımı.
- **Güvenlik (OpSec):** Hassas API verileri (`TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`) `.env` dosyası içinde izole edilmiştir; kod içerisine gömülmemiştir.
- **Depolama Yönetimi:** Disk optimizasyonu için en eski kayıtları otomatik temizleme mekanizması.

## Kurulum ve Çalıştırma

1. Gerekli kütüphaneleri yükleyin:
   `bash
   pip install opencv-python requests python-dotenv

2.Proje dizininde bir .env dosyası oluşturun ve Telegram API bilgilerinizi ekleyin:

TELEGRAM_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

3.Sistemi başlatın:

'bash
python guvenlikkamerasi.py
