🚀 AIShortsDownloader
<div align="center">

Belirlenen YouTube kanallarından Shorts videolarını yapay zekâ ile keşfeden, seçen ve yüksek kalitede indiren otomatik sistem.

</div>
📖 Genel Bakış

AIShortsDownloader, belirlenen YouTube kanallarından kısa videoları (Shorts) otomatik olarak bulmak, seçmek ve indirmek için tasarlanmış güçlü bir Python tabanlı sistemdir.
İçerik üreticileri, pazarlamacılar veya belirli kriterlere (anahtar kelimeler, kanal ID’leri) göre kısa video içeriği toplamak isteyen herkes için idealdir.
Sistem indirilen içerikleri yönetir, işlemleri kaydeder, raporlar oluşturur ve yedekleme işlevleriyle düzenli bir iş akışı sağlar.

✨ Özellikler

🎯 YouTube Kanal Takibi: Belirlenen kanal listesinden otomatik olarak video verilerini çeker.

💡 Akıllı Video Seçimi (AI): Kullanıcı tarafından belirlenen anahtar kelimelere ve kriterlere göre Shorts videolarını filtreleyip seçer.

⬇️ Yüksek Kaliteli Video İndirme: yt-dlp modülünü kullanarak seçilen Shorts videolarını en yüksek mevcut kalitede indirir.

🗄️ Yerel Veritabanı Yönetimi: SQLite veritabanı ile indirilen videoları takip eder, tekrar indirmeyi önler ve meta verileri yönetir.

⚙️ Kolay Yapılandırma: API anahtarları, kanallar, anahtar kelimeler ve yollar settings.json dosyası üzerinden kolayca düzenlenebilir.

📊 Otomatik Loglama & Raporlama: Tüm işlemleri kaydeder ve analiz için raporlar üretir.

💾 Yerleşik Yedekleme Sistemi: Belirlenen aralıklarla önemli verileri otomatik olarak yedekler.

🛠️ Teknoloji Yığını (Tech Stack)

Çalışma Ortamı:

Kütüphaneler:

Veritabanı:

Yapılandırma:

🚀 Hızlı Başlangıç
Gereksinimler

Python 3.x: Sisteminizde Python 3.x kurulu olduğundan emin olun.

python --version


YouTube Data API Anahtarı: Google Cloud Console üzerinden bir YouTube Data API v3 anahtarı alın.

Kurulum

Depoyu klonlayın

git clone https://github.com/yusufnightin/AIShortsDownloader.git
cd AIShortsDownloader


Bağımlılıkları yükleyin

pip install -r requirements.txt


Yapılandırma ayarlarını düzenleyin

settings.json dosyasını açın.

"YOUR_YOUTUBE_API_KEY" kısmını kendi YouTube Data API anahtarınızla değiştirin.

channel_ids alanına izlemek istediğiniz YouTube kanal ID’lerini ekleyin.

keywords kısmına seçilecek Shorts videoları için ilgili anahtar kelimeleri yazın.

download_path, log_level, max_shorts_per_channel ve backup_interval_days ayarlarını isteğinize göre düzenleyin.

Örnek settings.json:

{
  "youtube_api_key": "YOUR_YOUTUBE_API_KEY",
  "channel_ids": [
    "UC_x5XG1OV2P6uZZ5FSM9Ttw",
    "UC-9-kyTW8ZkZNDHQJ6FgpwQ"
  ],
  "keywords": [
    "eğitim",
    "kodlama",
    "komik anlar",
    "teknoloji inceleme"
  ],
  "download_path": "downloaded_shorts",
  "log_level": "INFO",
  "max_shorts_per_channel": 5,
  "backup_interval_days": 3
}


Programı çalıştırın

python main.py


Script, belirtilen kanalları izlemeye başlayacak, Shorts videolarını seçecek ve yapılandırmanıza göre indirecektir.

📁 Proje Yapısı
AIShortsDownloader/
├── main.py             # Ana uygulama mantığı ve giriş noktası
├── requirements.txt    # Python bağımlılık listesi
├── settings.json       # API anahtarı, kanal, anahtar kelime vb. yapılandırma
├── shorts_manager.db   # İndirilen Shorts videolarını takip eden SQLite veritabanı
├── backups/            # Veritabanı yedekleme dizini
├── logs/               # Uygulama log dosyaları
├── reports/            # Oluşturulan raporlar
└── README.md           # Proje dökümantasyonu

⚙️ Yapılandırma Değişkenleri

settings.json dosyası, AIShortsDownloader’ın çalışma şeklini belirleyen ana dosyadır.

Değişken	Açıklama	Örnek Değer	Zorunlu
youtube_api_key	Google YouTube Data API v3 anahtarınız.	AIzaSyD...	Evet
channel_ids	Shorts takibi yapılacak YouTube kanal ID listesi.	["UC_x...", "UC-..."]	Evet
keywords	Shorts seçimi için kullanılacak anahtar kelimeler.	["teknoloji", "review"]	Evet
download_path	İndirilen videoların kaydedileceği dizin.	"downloaded_shorts"	Evet
log_level	Log mesajlarının minimum seviyesi (DEBUG, INFO, vb.).	"INFO"	Hayır
max_shorts_per_channel	Her çalıştırmada kanal başına indirilecek maksimum Shorts sayısı.	5	Hayır
backup_interval_days	Veritabanı yedekleme sıklığı (gün).	7	Hayır
🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz!
Yeni özellik önerileri, hata düzeltmeleri veya geliştirme fikirleriniz varsa lütfen bir “issue” açın veya “pull request” gönderin.

Geliştirici Ortamı Kurulumu

Depoyu forklayın.

Fork’unuzu klonlayın:

git clone https://github.com/YOUR_USERNAME/AIShortsDownloader.git


Sanal ortam oluşturun:

python -m venv venv


Ortamı etkinleştirin:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Bağımlılıkları yükleyin:

pip install -r requirements.txt


Geliştirmelerinizi yapın ve test edin.

📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
Ayrıntılar için LICENSE
 dosyasına bakın.

🙏 Teşekkürler

yt-dlp
: Güçlü video indirme altyapısı.

Google API Python Client
: YouTube Data API ile kolay entegrasyon.

📞 Destek ve İletişim

🐛 Hata Bildirimi: GitHub Issues

<div align="center">

⭐ Yararlı bulduysanız bu depoya yıldız vermeyi unutmayın!

❤️ ile yapılmıştır — yusufnightin

</div>
