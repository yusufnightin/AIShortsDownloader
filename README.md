# 🤖 AIShorts – YouTube Shorts Downloader (AI Enhanced)

AIShorts, YouTube Shorts videolarını toplu şekilde indirmenizi, yönetmenizi ve raporlamanızı sağlayan **AI destekli** bir masaüstü uygulamasıdır.  
Tamamen Python ile geliştirilmiş olup, güçlü bir GUI arayüzü ve otomasyon altyapısına sahiptir.

---

## 🚀 Özellikler

- 🎥 **Toplu Shorts İndirme:** Belirli bir kanal veya bağlantı listesinden tüm videoları indirir.  
- 🤖 **AI Destekli Analiz:** İndirme geçmişini, video metadatalarını ve etkileşim oranlarını analiz ederek rapor oluşturur.  
- 💾 **Otomatik Yedekleme:** Veritabanı, rapor ve log dosyalarını otomatik olarak yedekler.  
- 🕒 **Zamanlayıcı & Otomasyon:** Belirlenen saat aralıklarında otomatik indirme başlatır.  
- 🎨 **Modern GUI:** `Tkinter` + `ttkbootstrap` temalı arayüz, dinamik temalar (dark/light).  
- ⚙️ **Ayar Kaydetme:** Tüm ayarlar `settings.json` dosyasında saklanır.  
- 🔐 **Veritabanı Desteği:** `SQLite` tabanlı veri yönetimi (`shorts_manager.db`).  
- 🌐 **Proxy Desteği:** IP koruması ve coğrafi erişim için proxy ile çalışma imkanı.  
- 📊 **AI Raporlama:** `raporlar/` klasöründe detaylı analiz raporları oluşturur.

---

## 🧩 Kullanılan Teknolojiler

| Bileşen | Açıklama | Kullanım Oranı |
|----------|-----------|----------------|
| 🐍 **Python** | Ana dil | 🟩🟩🟩🟩🟩 100% |
| 🎨 **Tkinter / ttkbootstrap** | GUI tasarımı | 🟩🟩🟩🟩🟨 80% |
| 🎥 **yt-dlp** | Video indirme altyapısı | 🟩🟩🟩🟩🟩 100% |
| 🧠 **AI (analiz & karar motoru)** | İndirme önerileri & rapor analizi | 🟩🟩🟩🟩⬜ 70% |
| 🗃️ **SQLite3** | Veritabanı & log sistemi | 🟩🟩🟩🟩🟩 100% |
| 🧰 **PIL / Requests / Logging** | Görsel işleme, ağ bağlantısı ve hata kayıtları | 🟩🟩🟩🟩⬜ 85% |

---

## 📦 Kurulum

### 1️⃣ Gerekli Bağımlılıkları Yükle:
pip install -r requirements.txt 


### 2️⃣ Programı Başlat:
Kodu kopyala
python main.py

###3️⃣ Ayarları Yapılandır:
Uygulama açıldıktan sonra:

İndirme klasörünü seçin

Kanal URL'sini ekleyin

Otomatik indirme ve AI rapor ayarlarını aktif edin

###⚙️ requirements.txt
yt-dlp
Pillow
requests
ttkbootstrap
concurrent-log-handler
sqlite3-binary
💡 sqlite3 Python’un içinde gömülü olarak gelir ancak bağımsız ortamlar için sqlite3-binary eklenmiştir.

###🧠 AI Bileşenleri Hakkında
AIShorts’un analiz motoru, indirme geçmişini ve rapor dosyalarını işleyerek:

En çok izlenen Shorts içeriklerini tespit eder

Ortalama izlenme süresi tahmini yapar

Gereksiz veya tekrar eden indirmeleri önler

Ayrıca sistem, kullanıcı davranışına göre öneri sunmak için hafif bir yapay zekâ modeli (lokal Python tabanlı) kullanır.

pie title "Kod Bileşen Dağılımı"
    "GUI (Tkinter/ttkbootstrap)" : 40
    "AI Analiz Modülü" : 20
    "yt-dlp Downloader" : 25
    "Veritabanı & Loglama" : 10
    "Yedekleme & Otomasyon" : 5
