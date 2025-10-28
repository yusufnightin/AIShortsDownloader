# 🚀 AIShortsDownloader

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/network)

[![GitHub issues](https://img.shields.io/github/issues/yusufnightin/AIShortsDownloader?style=for-the-badge)](https://github.com/yusufnightin/AIShortsDownloader/issues)

[![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)

**Belirli kanallardan YouTube Shorts keşfini, akıllı seçimi ve yüksek kaliteli indirmeyi otomatikleştirin.**

</div>

## 📖 Genel Bakış

`AIShortsDownloader`, belirli YouTube kanallarından kısa videoları bulma, seçme ve indirme sürecini otomatikleştirmek için tasarlanmış, Python tabanlı, güçlü bir sistemdir. İçerik oluşturucular, pazarlamacılar veya analiz, düzenleme veya yaratıcı projeler için belirli kriterlere (anahtar kelimeler, kanal kimlikleri) göre ilgili kısa video içerikleri toplaması gereken herkes için tasarlanmıştır. Sistem, indirilen içerikleri yönetir, işlemleri kaydeder, raporlar oluşturur ve yedekleme işlevleri sunarak verimli ve düzenli bir iş akışı sağlar.

## ✨ Özellikler

- 🎯 **YouTube Kanal İzleme**: Yapılandırılabilir bir YouTube kanalları listesinden video verilerini otomatik olarak alır.
- 💡 **Akıllı Kısa Video Seçimi**: Kullanıcı tanımlı anahtar kelimeler ve kriterlere göre kısa videoları filtreler ve seçer, alaka düzeyini garanti eder.
- ⬇️ **Yüksek Kaliteli Video İndirme**: Seçilen YouTube kısa videolarını mevcut en iyi kalitede indirmek için `yt-dlp` kullanır.
- 🗄️ **Yerel Veritabanı Yönetimi**: İndirilen kısa videoları izlemek, kopyaları önlemek ve meta verileri yönetmek için SQLite kullanır.
- ⚙️ **Son Derece Yapılandırılabilir Ayarlar**: API anahtarları, kanallar, anahtar kelimeler ve yollar dahil tüm operasyonel parametreler `settings.json` aracılığıyla kolayca yönetilir. - 📊 **Otomatik Kayıt ve Raporlama**: Tüm operasyonları ve faaliyetleri kaydeder ve denetim ve analiz için raporlar oluşturur.
- 💾 **Yerleşik Yedekleme Mekanizması**: Kritik verileri yapılandırılabilir aralıklarla otomatik olarak yedekler.

## 🛠️ Teknoloji Yığını

**Çalışma Süresi:**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Kütüphaneler:**

[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-green?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)

[![Google API Python Client](https://img.shields.io/badge/Google_API_Client-Python-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/googleapis/google-api-python-client)

**Database:**

[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)

**Yapılandırma:**

[![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)](https://www.json.org/json-en.html)

## 🚀 Quick Start

### Önkoşullar
- **Python 3.x**: Sisteminizde Python 3.x'in yüklü olduğundan emin olun.
```bash
python --version
```

### Kurulum

1. **Depoyu kopyala**
```bash
git clone https://github.com/yusufnightin/AIShortsDownloader.git
cd AIShortsDownloader
```

2. **Bağımlılıkları yükle**
```bash
pip install -r requirements.txt
```
    ```

4. **İndiriciyi çalıştırın**
```bash
python main.py
```
Komut dosyası, yapılandırmanıza bağlı olarak kanalları izlemeye, kısa videoları seçmeye ve indirmeye başlayacaktır.

## 📁 Proje Yapısı

```
AIShortsDownloader/
├── main.py # Ana uygulama mantığı ve giriş noktası
├── requirements.txt # Python bağımlılık listesi
├── settings.json # API anahtarları, kanallar, anahtar kelimeler vb. için yapılandırma dosyası
├── shorts_manager.db # İndirilen short'ları izlemek için SQLite veritabanı
├── backups/ # Veritabanı yedekleri dizini
├── logs/ # Uygulama günlük dosyaları dizini
├── reports/ # Oluşturulan operasyonel raporlar dizini
└── README.md # Proje dokümantasyonu
```


## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! İyileştirmeler, yeni özellikler veya hata düzeltmeleri için önerileriniz varsa, lütfen bir sorun açın veya bir çekme isteği gönderin.

### Geliştirme Kurulumu
1. Depoyu çatallandırın.
2. Çatallandırılmış deponuzu klonlayın: `git clone https://github.com/YOUR_USERNAME/AIShortsDownloader.git`
3. Sanal bir ortam oluşturun: `python -m venv venv`
4. Ortamı etkinleştirin:
* Windows: `.\venv\Scripts\activate`
* macOS/Linux: `source venv/bin/activate`
5. Bağımlılıkları yükleyin: `pip install -r requirements.txt`
6. Değişikliklerinizi yapın ve test edildiklerinden emin olun.

## 📄 Lisans

Bu proje MIT Lisansı kapsamındadır - ayrıntılar için [LICENSE](LICENSE) dosyasına bakın. <!-- TODO: LICENSE dosyası ekle -->

## 🙏 Teşekkürler

- Güçlü video indirme yetenekleri için [yt-dlp](https://github.com/yt-dlp/yt-dlp).
- YouTube Veri API'siyle sorunsuz etkileşim için [Google API Python İstemcisi](https://github.com/googleapis/google-api-python-client).

## 📞 Destek ve İletişim

- 🐛 Sorunlar: [GitHub Sorunları](https://github.com/yusufnightin/AIShortsDownloader/issues)

---

<div align="center">

**⭐ Faydalı bulduysanız bu depoya yıldız ekleyin!**

[yusufnightin](https://github.com/yusufnightin) & AI tarafından ❤️ ile yapıldı

</div>

