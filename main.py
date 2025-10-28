import os
import yt_dlp
import threading
import time
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, filedialog, messagebox, Canvas, Frame, Scrollbar, NW, Text, Toplevel, Listbox, MULTIPLE, END, BooleanVar
from tkinter.ttk import Progressbar, Notebook, Style, Combobox, Checkbutton, Treeview, Separator
from PIL import Image, ImageTk, ImageOps
import requests
from io import BytesIO
import concurrent.futures
import queue
import json
import webbrowser
import sqlite3
import hashlib
import re
import sys
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import zipfile
import shutil

# ----------------- Logging Kurulumu -----------------
def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                os.path.join(log_dir, 'shorts_downloader.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )

setup_logging()

# ----------------- Pencere -----------------
root = Tk()
root.title("🚀 YouTube Shorts İndirici Ultimate Pro")
root.geometry("1400x900")
root.configure(bg='#0d1117')

# ----------------- Değişkenler -----------------
channel_var = StringVar()
count_var = IntVar(value=10)
folder_var = StringVar()
interval_var = IntVar(value=300)
theme_var = StringVar(value="dark")
quality_var = StringVar(value="720p")
download_audio_var = IntVar(value=1)
auto_download_var = IntVar(value=0)
schedule_enabled_var = IntVar(value=0)
start_time_var = StringVar(value="09:00")
end_time_var = StringVar(value="18:00")
max_storage_var = IntVar(value=1024)  # GB
language_var = StringVar(value="tr")
notification_var = IntVar(value=1)
proxy_enabled_var = IntVar(value=0)
proxy_url_var = StringVar()

selected_shorts = []
downloaded_urls = set()
shorts_list = []
thumbnail_images = {}
thumbnail_queue = queue.Queue()
is_loading = False
channels_list = []
download_history = []
scheduled_tasks = []
is_paused = False

# ----------------- Veritabanı -----------------
def init_database():
    conn = sqlite3.connect('shorts_manager.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            title TEXT,
            channel TEXT,
            duration INTEGER,
            download_date TEXT,
            file_path TEXT,
            file_size INTEGER,
            status TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            name TEXT,
            last_checked TEXT,
            enabled INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_database()

# ----------------- Tema Renkleri -----------------
THEMES = {
    "dark": {
        "bg": "#0d1117",
        "fg": "#ffffff",
        "accent": "#ff375f",
        "secondary": "#161b22",
        "text": "#8b949e",
        "button_bg": "#ff375f",
        "button_fg": "#ffffff",
        "canvas_bg": "#161b22",
        "card_bg": "#21262d",
        "hover_bg": "#30363d",
        "success": "#3fb950",
        "warning": "#d29922",
        "error": "#f85149"
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#1f2328",
        "accent": "#ff375f",
        "secondary": "#f6f8fa",
        "text": "#656d76",
        "button_bg": "#ff375f",
        "button_fg": "#ffffff",
        "canvas_bg": "#ffffff",
        "card_bg": "#f6f8fa",
        "hover_bg": "#eaeef2",
        "success": "#1a7f37",
        "warning": "#9a6700",
        "error": "#cf222e"
    },
    "blue": {
        "bg": "#0a1929",
        "fg": "#e6f7ff",
        "accent": "#1890ff",
        "secondary": "#132f4c",
        "text": "#8ca0b3",
        "button_bg": "#1890ff",
        "button_fg": "#ffffff",
        "canvas_bg": "#132f4c",
        "card_bg": "#173553",
        "hover_bg": "#1e4a6e",
        "success": "#52c41a",
        "warning": "#faad14",
        "error": "#ff4d4f"
    }
}

# ----------------- Ayarlar Yönetimi -----------------
def load_settings():
    global channels_list
    try:
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        
        # Ayarlar
        cursor.execute("SELECT key, value FROM settings")
        settings = {row[0]: row[1] for row in cursor.fetchall()}
        
        folder_var.set(settings.get("download_folder", ""))
        theme_var.set(settings.get("theme", "dark"))
        quality_var.set(settings.get("quality", "720p"))
        download_audio_var.set(int(settings.get("download_audio", "1")))
        auto_download_var.set(int(settings.get("auto_download", "0")))
        count_var.set(int(settings.get("max_videos", "10000")))
        interval_var.set(int(settings.get("check_interval", "300")))
        language_var.set(settings.get("language", "tr"))
        notification_var.set(int(settings.get("notifications", "1")))
        proxy_enabled_var.set(int(settings.get("proxy_enabled", "0")))
        proxy_url_var.set(settings.get("proxy_url", ""))
        
        # Kanallar
        cursor.execute("SELECT url, name, enabled FROM channels")
        channels_list = [row[0] for row in cursor.fetchall() if row[2]]
        
        conn.close()
        apply_theme()
        update_channels_listbox()
        
    except Exception as e:
        logging.error(f"Ayarlar yüklenirken hata: {e}")

def save_settings():
    try:
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        
        settings = {
            "download_folder": folder_var.get(),
            "theme": theme_var.get(),
            "quality": quality_var.get(),
            "download_audio": str(download_audio_var.get()),
            "auto_download": str(auto_download_var.get()),
            "max_videos": str(count_var.get()),
            "check_interval": str(interval_var.get()),
            "language": language_var.get(),
            "notifications": str(notification_var.get()),
            "proxy_enabled": str(proxy_enabled_var.get()),
            "proxy_url": proxy_url_var.get()
        }
        
        for key, value in settings.items():
            cursor.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, value)
            )
        
        # Kanalları kaydet
        for channel_url in channels_list:
            cursor.execute(
                "INSERT OR REPLACE INTO channels (url, name, enabled) VALUES (?, ?, 1)",
                (channel_url, get_channel_name(channel_url))
            )
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logging.error(f"Ayarlar kaydedilirken hata: {e}")

def get_channel_name(url):
    """URL'den kanal adını çıkar"""
    try:
        if '/@' in url:
            return url.split('/@')[-1].split('/')[0]
        elif '/channel/' in url:
            return url.split('/channel/')[-1].split('/')[0]
        else:
            return url
    except:
        return "Bilinmeyen"

# ----------------- Tema Yönetimi -----------------
def apply_theme():
    theme = theme_var.get()
    colors = THEMES[theme]
    
    style = Style()
    style.theme_use('clam')
    
    # Stilleri yapılandır
    style.configure("TNotebook", background=colors["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", 
                   background=colors["secondary"],
                   foreground=colors["fg"],
                   padding=[20, 5],
                   focuscolor=colors["secondary"])
    style.map("TNotebook.Tab", 
             background=[("selected", colors["accent"])],
             foreground=[("selected", colors["button_fg"])])
    
    style.configure("Horizontal.TProgressbar", 
                   background=colors["accent"],
                   troughcolor=colors["secondary"])
    
    style.configure("Treeview",
                   background=colors["card_bg"],
                   foreground=colors["fg"],
                   fieldbackground=colors["card_bg"])
    style.configure("Treeview.Heading",
                   background=colors["secondary"],
                   foreground=colors["fg"])
    
    # Widget renklerini güncelle
    update_widget_colors(colors)

def update_widget_colors(colors):
    for widget in root.winfo_children():
        update_widget_tree(widget, colors)

def update_widget_tree(widget, colors):
    try:
        if isinstance(widget, (Label, Button)):
            if widget.winfo_class() not in ['TButton', 'TCheckbutton']:
                widget.configure(bg=colors["bg"], fg=colors["fg"])
        elif isinstance(widget, (Entry, Text)):
            widget.configure(bg=colors["card_bg"], fg=colors["text"], 
                           insertbackground=colors["fg"])
        elif isinstance(widget, (Canvas, Frame)):
            widget.configure(bg=colors["bg"])
        elif isinstance(widget, Listbox):
            widget.configure(bg=colors["card_bg"], fg=colors["text"],
                           selectbackground=colors["accent"])
    except:
        pass
    
    for child in widget.winfo_children():
        update_widget_tree(child, colors)

def toggle_theme():
    """Temayı değiştir"""
    current_theme = theme_var.get()
    themes = list(THEMES.keys())
    current_index = themes.index(current_theme)
    next_index = (current_index + 1) % len(themes)
    theme_var.set(themes[next_index])
    apply_theme()
    save_settings()

# ----------------- Gelişmiş Fonksiyonlar -----------------
def show_analytics():
    """Analiz paneli"""
    analytics_window = Toplevel(root)
    analytics_window.title("📊 Analiz Paneli")
    analytics_window.geometry("1000x700")
    analytics_window.configure(bg=THEMES[theme_var.get()]["bg"])
    
    # İstatistikler
    conn = sqlite3.connect('shorts_manager.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM downloads")
    total_downloads = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT channel) FROM downloads")
    total_channels = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(file_size) FROM downloads")
    total_size = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM channels")
    tracked_channels = cursor.fetchone()[0]
    
    conn.close()
    
    # İstatistik çerçevesi
    stats_frame = Frame(analytics_window, bg=THEMES[theme_var.get()]["bg"])
    stats_frame.pack(fill="x", padx=20, pady=20)
    
    stats_data = [
        ("📥 Toplam İndirme", f"{total_downloads:,}"),
        ("📊 Toplam Kanal", f"{total_channels}"),
        ("💾 Kullanılan Depolama", f"{total_size/(1024**3):.2f} GB"),
        ("👁️ Takip Edilen Kanallar", f"{tracked_channels}")
    ]
    
    for i, (label, value) in enumerate(stats_data):
        stat_frame = Frame(stats_frame, bg=THEMES[theme_var.get()]["card_bg"], relief="raised", bd=1)
        stat_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        Label(stat_frame, text=label, font=("Arial", 10), 
              bg=THEMES[theme_var.get()]["card_bg"], fg=THEMES[theme_var.get()]["text"]).pack(pady=5)
        Label(stat_frame, text=value, font=("Arial", 16, "bold"), 
              bg=THEMES[theme_var.get()]["card_bg"], fg=THEMES[theme_var.get()]["accent"]).pack(pady=5)

    # Son indirmeler
    recent_frame = Frame(analytics_window, bg=THEMES[theme_var.get()]["bg"])
    recent_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    Label(recent_frame, text="Son İndirmeler", font=("Arial", 14, "bold"),
          bg=THEMES[theme_var.get()]["bg"], fg=THEMES[theme_var.get()]["fg"]).pack(anchor="w")
    
    # Son indirmeler için Treeview
    tree = Treeview(recent_frame, columns=("Başlık", "Kanal", "Tarih", "Boyut"), show="headings")
    tree.heading("Başlık", text="Başlık")
    tree.heading("Kanal", text="Kanal")
    tree.heading("Tarih", text="Tarih")
    tree.heading("Boyut", text="Boyut")
    
    tree.pack(fill="both", expand=True)

def backup_data():
    """Veritabanı ve ayarların yedeğini oluştur"""
    try:
        backup_dir = "yedekler"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"yedek_{timestamp}.zip")
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            zipf.write('shorts_manager.db')
            if os.path.exists('settings.json'):
                zipf.write('settings.json')
        
        log_area.insert(END, f"✅ Yedek oluşturuldu: {backup_file}\n")
        messagebox.showinfo("Yedekleme", f"Yedek başarıyla oluşturuldu!\n{backup_file}")
        
    except Exception as e:
        messagebox.showerror("Yedekleme Hatası", f"Yedek oluşturulamadı: {e}")

def restore_data():
    """Yedekten geri yükle"""
    file_path = filedialog.askopenfilename(
        title="Yedek Dosyasını Seç",
        filetypes=[("ZIP dosyaları", "*.zip")]
    )
    
    if file_path:
        try:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall('.')
            
            load_settings()
            log_area.insert(END, "✅ Yedek başarıyla geri yüklendi\n")
            messagebox.showinfo("Geri Yükleme", "Yedek başarıyla geri yüklendi!")
            
        except Exception as e:
            messagebox.showerror("Geri Yükleme Hatası", f"Geri yükleme başarısız: {e}")

def schedule_downloads():
    """Otomatik indirmeleri planla"""
    if schedule_enabled_var.get():
        start_time = start_time_var.get()
        end_time = end_time_var.get()
        
        log_area.insert(END, f"⏰ İndirme planlandı: {start_time} - {end_time}\n")
        
        # Planlanmış görev
        def scheduled_task():
            while schedule_enabled_var.get():
                now = datetime.now().strftime("%H:%M")
                if start_time <= now <= end_time and not is_paused:
                    fetch_all_channels()
                    time.sleep(interval_var.get())
                time.sleep(60)  # Her dakika kontrol et
        
        threading.Thread(target=scheduled_task, daemon=True).start()

def check_storage():
    """Kullanılabilir depolama alanını kontrol et"""
    download_folder = folder_var.get()
    if download_folder and os.path.exists(download_folder):
        total, used, free = shutil.disk_usage(download_folder)
        free_gb = free // (2**30)
        
        if free_gb < 5:  # 5GB'tan az boş alan
            show_notification("Depolama Uyarısı", f"Düşük disk alanı: {free_gb}GB boş")
            return False
    return True

def show_notification(title, message):
    """Sistem bildirimi göster"""
    if notification_var.get():
        try:
            # Şimdilik basit messagebox
            messagebox.showwarning(title, message)
        except:
            pass

def optimize_database():
    """Veritabanı performansını optimize et"""
    try:
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        cursor.execute("VACUUM")
        cursor.execute("ANALYZE")
        conn.close()
        
        log_area.insert(END, "✅ Veritabanı optimize edildi\n")
        messagebox.showinfo("Optimizasyon", "Veritabanı başarıyla optimize edildi!")
        
    except Exception as e:
        messagebox.showerror("Optimizasyon Hatası", f"Optimizasyon başarısız: {e}")

def export_subscriptions():
    """Kanalları YouTube abonelik dosyasına aktar"""
    try:
        file_path = filedialog.asksaveasfilename(
            title="Abonelikleri Dışa Aktar",
            defaultextension=".csv",
            filetypes=[("CSV dosyaları", "*.csv")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Kanal URL,Kanal Adı\n")
                for channel in channels_list:
                    f.write(f"{channel},{get_channel_name(channel)}\n")
            
            log_area.insert(END, f"✅ Abonelikler dışa aktarıldı: {file_path}\n")
            messagebox.showinfo("Dışa Aktarma", "Abonelikler başarıyla dışa aktarıldı!")
            
    except Exception as e:
        messagebox.showerror("Dışa Aktarma Hatası", f"Dışa aktarma başarısız: {e}")

def bulk_operations():
    """Toplu işlemler penceresi"""
    bulk_window = Toplevel(root)
    bulk_window.title("🛠️ Toplu İşlemler")
    bulk_window.geometry("600x400")
    bulk_window.configure(bg=THEMES[theme_var.get()]["bg"])
    
    # Toplu işlemler çerçevesi
    bulk_frame = Frame(bulk_window, bg=THEMES[theme_var.get()]["bg"])
    bulk_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    operations = [
        ("🔄 Tüm Kanalları Güncelle", update_all_channels),
        ("🧹 Yinelenenleri Temizle", clean_duplicates),
        ("📊 Rapor Oluştur", generate_report),
        ("🗑️ Geçmişi Temizle", clear_download_history),
        ("🔍 Bozuk Bağlantıları Kontrol Et", check_broken_links)
    ]
    
    for i, (text, command) in enumerate(operations):
        Button(bulk_frame, text=text, command=command,
               bg=THEMES[theme_var.get()]["secondary"],
               fg=THEMES[theme_var.get()]["fg"],
               font=("Arial", 11),
               pady=10).pack(fill="x", pady=5)

def update_all_channels():
    """Tüm kanal bilgilerini güncelle"""
    log_area.insert(END, "🔄 Tüm kanallar güncelleniyor...\n")
    fetch_all_channels()

def clean_duplicates():
    """Yinelenen videoları kaldır"""
    try:
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM downloads 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM downloads 
                GROUP BY video_id
            )
        ''')
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        log_area.insert(END, f"✅ {deleted_count} yinelenen kaldırıldı\n")
        messagebox.showinfo("Yinelenenleri Temizle", f"{deleted_count} yinelenen kayıt kaldırıldı!")
        
    except Exception as e:
        messagebox.showerror("Temizleme Hatası", f"Temizleme başarısız: {e}")

def generate_report():
    """İndirme raporu oluştur"""
    try:
        report_dir = "raporlar"
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(report_dir, f"rapor_{timestamp}.txt")
        
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM downloads")
        total_downloads = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT channel) FROM downloads")
        total_channels = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(file_size) FROM downloads")
        total_size = cursor.fetchone()[0] or 0
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("YouTube Shorts İndirici Raporu\n")
            f.write("=" * 40 + "\n")
            f.write(f"Oluşturulma: {datetime.now()}\n")
            f.write(f"Toplam İndirme: {total_downloads}\n")
            f.write(f"Toplam Kanal: {total_channels}\n")
            f.write(f"Toplam Boyut: {total_size/(1024**3):.2f} GB\n")
            f.write(f"Takip Edilen Kanallar: {len(channels_list)}\n")
        
        conn.close()
        
        log_area.insert(END, f"📊 Rapor oluşturuldu: {report_file}\n")
        messagebox.showinfo("Rapor", f"Rapor başarıyla oluşturuldu!\n{report_file}")
        
    except Exception as e:
        messagebox.showerror("Rapor Hatası", f"Rapor oluşturma başarısız: {e}")

def clear_download_history():
    """İndirme geçmişini temizle"""
    if messagebox.askyesno("Onay", "Tüm indirme geçmişini temizlemek istediğinizden emin misiniz?"):
        try:
            conn = sqlite3.connect('shorts_manager.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM downloads")
            conn.commit()
            conn.close()
            
            downloaded_urls.clear()
            log_area.insert(END, "✅ İndirme geçmişi temizlendi\n")
            
        except Exception as e:
            messagebox.showerror("Temizleme Hatası", f"Temizleme başarısız: {e}")

def check_broken_links():
    """Bozuk video bağlantılarını kontrol et"""
    log_area.insert(END, "🔍 Bozuk bağlantılar kontrol ediliyor...\n")
    # Bozuk bağlantı kontrolü implementasyonu
    # Her video URL'sine erişmeyi deneyip hata dönenleri işaretleme

def advanced_search():
    """Gelişmiş arama penceresi"""
    search_window = Toplevel(root)
    search_window.title("🔍 Gelişmiş Arama")
    search_window.geometry("500x300")
    search_window.configure(bg=THEMES[theme_var.get()]["bg"])
    
    search_frame = Frame(search_window, bg=THEMES[theme_var.get()]["bg"])
    search_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Arama kriterleri
    Label(search_frame, text="Arama Terimi:", bg=THEMES[theme_var.get()]["bg"], 
          fg=THEMES[theme_var.get()]["fg"]).pack(anchor="w")
    search_entry = Entry(search_frame, width=50)
    search_entry.pack(fill="x", pady=5)
    
    def perform_search():
        term = search_entry.get()
        log_area.insert(END, f"🔍 Aranıyor: {term}\n")
    
    Button(search_frame, text="🔍 Ara", command=perform_search,
           bg=THEMES[theme_var.get()]["accent"],
           fg=THEMES[theme_var.get()]["button_fg"]).pack(pady=10)

def show_instructions():
    """Kullanım talimatlarını göster"""
    instructions = Toplevel(root)
    instructions.title("📖 Kullanım Kılavuzu")
    instructions.geometry("600x400")
    instructions.configure(bg=THEMES[theme_var.get()]["bg"])
    
    text_frame = Frame(instructions, bg=THEMES[theme_var.get()]["bg"])
    text_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    text_widget = Text(text_frame, wrap="word", font=("Arial", 10), 
                      bg=THEMES[theme_var.get()]["card_bg"], 
                      fg=THEMES[theme_var.get()]["text"],
                      padx=15, pady=15)
    
    scrollbar = Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    instructions_text = """
🚀 YouTube Shorts İndirici Ultimate Pro

📥 NASIL KULLANILIR:
1. Kanallar sekmesinden kanal ekleyin
2. 'Tüm Kanalları Getir' butonuna tıklayarak shorts'ları alın
3. Videoları seçin ve 'Seçileni İndir' butonuna tıklayın
4. İlerlemeyi Loglar sekmesinden takip edin

⚡ ÖZELLİKLER:
• Toplu kanal yönetimi
• Gelişmiş planlama
• Analiz ve raporlama
• Yedekleme ve geri yükleme
• Çoklu tema seçenekleri
• Veritabanı optimizasyonu

🎯 TEMEL İŞLEMLER:
• Kanal eklemek için URL'yi girin ve "Kanal Ekle" butonuna tıklayın
• TXT dosyasından toplu kanal ekleyebilirsiniz
• Shorts'ları listeledikten sonra istediklerinizi seçip indirebilirsiniz
• Ayarlardan indirme kalitesi ve tema seçebilirsiniz
    """
    
    text_widget.insert("1.0", instructions_text)
    text_widget.config(state="disabled")
    
    Button(instructions, text="✅ Anladım", command=instructions.destroy,
           bg=THEMES[theme_var.get()]["accent"],
           fg=THEMES[theme_var.get()]["button_fg"]).pack(pady=10)

# ----------------- Kanal Yönetimi -----------------
def load_channels_from_file():
    """TXT dosyasından kanal listesi yükle"""
    file_path = filedialog.askopenfilename(
        title="Kanal Listesi Seç",
        filetypes=[("Text dosyaları", "*.txt"), ("CSV dosyaları", "*.csv"), ("Tüm dosyalar", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_channels = [line.strip() for line in f.readlines() if line.strip() and 'youtube.com' in line]
            
            channels_list.extend(new_channels)
            update_channels_listbox()
            save_settings()
            
            log_area.insert(END, f"✅ {len(new_channels)} kanal eklendi\n")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okunamadı: {e}")

def update_channels_listbox():
    """Kanal listbox'ını güncelle"""
    if 'channels_listbox' in globals():
        channels_listbox.delete(0, END)
        for channel in channels_list:
            channels_listbox.insert(END, f"{get_channel_name(channel)} - {channel}")

def add_channel_manual():
    """Manuel kanal ekle"""
    channel_url = channel_var.get().strip()
    if channel_url and channel_url not in channels_list:
        channels_list.append(channel_url)
        update_channels_listbox()
        channel_var.set("")
        save_settings()
        log_area.insert(END, f"✅ Kanal eklendi: {get_channel_name(channel_url)}\n")

def remove_selected_channels():
    """Seçili kanalları sil"""
    if 'channels_listbox' in globals():
        selected = channels_listbox.curselection()
        if not selected:
            messagebox.showwarning("Uyarı", "Silmek için kanal seçin")
            return
            
        for index in selected[::-1]:
            channel_name = get_channel_name(channels_list[index])
            channels_list.pop(index)
            channels_listbox.delete(index)
            log_area.insert(END, f"🗑️ Kanal silindi: {channel_name}\n")
        
        save_settings()

# ----------------- Shorts Yönetimi -----------------
def fetch_all_channels():
    """Tüm kanalları listele"""
    if not channels_list:
        messagebox.showwarning("Uyarı", "Kanal listesi boş")
        return
    
    global shorts_list
    shorts_list = []
    
    def fetch_thread():
        total_shorts = 0
        for channel_url in channels_list:
            if is_paused:
                break
                
            try:
                log_area.insert(END, f"🔄 {get_channel_name(channel_url)} işleniyor...\n")
                log_area.see(END)
                
                working_url = channel_url
                if '/shorts' not in channel_url:
                    if '/@' in channel_url:
                        working_url = channel_url.rstrip('/') + '/shorts'
                    elif '/channel/' in channel_url:
                        working_url = channel_url.rstrip('/') + '/shorts'
                
                ydl_opts = {
                    'quiet': True,
                    'skip_download': True,
                    'extract_flat': True,
                    'playlistend': 30,
                    'no_warnings': True,
                }
                
                # Proxy desteği
                if proxy_enabled_var.get() and proxy_url_var.get():
                    ydl_opts['proxy'] = proxy_url_var.get()
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(working_url, download=False)
                    videos = info.get('entries', []) or []
                
                for v in videos:
                    if v and v.get('url') and v.get('url') not in [s.get('url') for s in shorts_list]:
                        # Metadata ekle
                        v['channel'] = get_channel_name(channel_url)
                        v['channel_url'] = channel_url
                        v['added_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        shorts_list.append(v)
                        total_shorts += 1
                
            except Exception as e:
                log_area.insert(END, f"❌ {get_channel_name(channel_url)} hata: {str(e)[:50]}\n")
        
        root.after(0, lambda: finish_fetch_all(total_shorts))
    
    threading.Thread(target=fetch_thread, daemon=True).start()

def finish_fetch_all(total_shorts):
    """Toplu listeleme tamamlandı"""
    load_short_list_advanced()
    log_area.insert(END, f"✅ {len(channels_list)} kanaldan {total_shorts} shorts bulundu\n")
    status_label.config(text=f"🎯 {total_shorts} shorts listelendi")
    
    # Otomatik indirme aktifse
    if auto_download_var.get() and total_shorts > 0:
        download_all_videos()

def load_short_list_advanced():
    """Gelişmiş liste yükleme"""
    global thumbnail_images
    if 'canvas' in globals():
        canvas.delete("all")
    
    if not shorts_list:
        if 'canvas' in globals():
            canvas.create_text(400, 50, text="❌ Shorts bulunamadı", font=("Arial", 12), 
                              fill=THEMES[theme_var.get()]["fg"])
        return
    
    if 'canvas' in globals():
        y_pos = 20
        
        for idx, v in enumerate(shorts_list):
            url = v.get('url', '')
            title = v.get('title', 'Bilinmeyen Başlık')[:50] + "..." if len(v.get('title', '')) > 50 else v.get('title', 'Bilinmeyen Başlık')
            duration = v.get('duration', 'N/A')
            channel = v.get('channel', 'Bilinmeyen Kanal')
            
            # Seçim kutusu
            is_selected = url in selected_shorts
            checkbox_color = THEMES[theme_var.get()]["accent"] if is_selected else THEMES[theme_var.get()]["text"]
            canvas.create_rectangle(20, y_pos, 40, y_pos+20, outline=checkbox_color, width=2, fill=checkbox_color if is_selected else "")
            
            # Video bilgileri
            canvas.create_text(60, y_pos, anchor=NW, text=f"{idx+1}. {title}", 
                              width=800, font=("Arial", 10, "bold"), fill=THEMES[theme_var.get()]["fg"])
            
            canvas.create_text(60, y_pos + 22, anchor=NW, text=f"⏱️ {duration}s | 📺 {channel} | 🔗 {url}", 
                              width=800, font=("Arial", 8), fill=THEMES[theme_var.get()]["text"])
            
            # Butonlar
            watch_btn = Button(canvas, text="🎬 İzle", command=lambda u=url: watch_video(u),
                             bg=THEMES[theme_var.get()]["secondary"], fg=THEMES[theme_var.get()]["fg"],
                             font=("Arial", 7), padx=5, pady=2)
            canvas.create_window(800, y_pos, anchor=NW, window=watch_btn)
            
            download_btn = Button(canvas, text="⬇️ İndir", command=lambda u=url: download_single_video(u),
                                bg=THEMES[theme_var.get()]["secondary"], fg=THEMES[theme_var.get()]["fg"],
                                font=("Arial", 7), padx=5, pady=2)
            canvas.create_window(870, y_pos, anchor=NW, window=download_btn)
            
            # Tıklama alanı
            canvas.create_rectangle(20, y_pos, 950, y_pos+40, outline="", tags=f"video_{idx}")
            canvas.tag_bind(f"video_{idx}", "<Button-1>", lambda e, idx=idx: toggle_video_selection(idx))
            
            y_pos += 50
        
        canvas.config(scrollregion=canvas.bbox("all"))
    
    status_label.config(text=f"📊 {len(shorts_list)} shorts listelendi | {len(selected_shorts)} seçili")

def toggle_video_selection(index):
    """Video seçimini değiştir"""
    if index < len(shorts_list):
        url = shorts_list[index].get('url')
        if url in selected_shorts:
            selected_shorts.remove(url)
        else:
            selected_shorts.append(url)
        load_short_list_advanced()

def watch_video(url):
    """Videoyu tarayıcıda aç"""
    webbrowser.open(url)

def download_single_video(url):
    """Tek video indir"""
    download_shorts_advanced([url])

def download_selected_videos():
    """Seçili videoları indir"""
    if not selected_shorts:
        messagebox.showwarning("Uyarı", "İndirilecek video seçmediniz")
        return
    download_shorts_advanced(selected_shorts)

def download_all_videos():
    """Tüm videoları indir"""
    if not shorts_list:
        messagebox.showwarning("Uyarı", "Listede video yok")
        return
    urls = [v.get('url') for v in shorts_list if v.get('url')]
    download_shorts_advanced(urls)

def download_shorts_advanced(urls_to_download):
    """Gelişmiş indirme"""
    if not check_storage():
        messagebox.showwarning("Depolama Uyarısı", "Düşük disk alanı! İndirme duraklatıldı.")
        return
        
    download_folder = folder_var.get()
    if not download_folder:
        messagebox.showerror("Hata", "Lütfen bir klasör seçin")
        return

    max_videos = min(int(count_var.get()), 50)
    urls_to_download = [url for url in urls_to_download if url not in downloaded_urls][:max_videos]

    if not urls_to_download:
        messagebox.showinfo("Bilgi", "İndirilecek yeni video yok")
        return

    today_folder = os.path.join(download_folder, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(today_folder, exist_ok=True)

    progress['value'] = 0
    progress['maximum'] = len(urls_to_download)
    status_label.config(text=f"⬇️ {len(urls_to_download)} video indiriliyor...")

    def progress_hook(d):
        if d['status'] == 'finished':
            progress['value'] += 1
            percentage = int((progress['value']/progress['maximum'])*100)
            status_label.config(text=f"⬇️ %{percentage} ({progress['value']}/{progress['maximum']})")
            
            # İndirme geçmişine ekle
            info = d['info_dict']
            downloaded_urls.add(info['webpage_url'])
            
            # Veritabanına kaydet
            save_download_history(info)
            
            filename = info.get('title', 'Bilinmeyen')
            log_area.insert(END, f"✅ {filename}\n")
            log_area.see(END)
            
        elif d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            status_label.config(text=f"⬇️ {percent} - {speed}")

    # Gelişmiş indirme seçenekleri
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' if download_audio_var.get() else 'best[height<=1080]',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(today_folder, '%(title).100s.%(ext)s'),
        'ignoreerrors': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'writethumbnail': False,
        'continuedl': True,
    }

    # Proxy desteği
    if proxy_enabled_var.get() and proxy_url_var.get():
        ydl_opts['proxy'] = proxy_url_var.get()

    # Ses işleme
    if download_audio_var.get():
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls_to_download)
        
        status_label.config(text="✅ İndirme tamamlandı!")
        log_area.insert(END, f"🎉 {len(urls_to_download)} video başarıyla indirildi!\n")
        load_short_list_advanced()
        
    except Exception as e:
        status_label.config(text="❌ İndirme hatası!")
        log_area.insert(END, f"❌ Hata: {str(e)[:100]}\n")

def save_download_history(info):
    """İndirme bilgilerini veritabanına kaydet"""
    try:
        conn = sqlite3.connect('shorts_manager.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO downloads 
            (video_id, title, channel, duration, download_date, file_path, file_size, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            info.get('id'),
            info.get('title'),
            info.get('uploader'),
            info.get('duration'),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            info.get('_filename'),
            info.get('filesize', 0),
            'tamamlandı'
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logging.error(f"Geçmiş kaydetme hatası: {e}")

# ----------------- GUI -----------------
def create_main_gui():
    # Başlık
    header_frame = Frame(root, bg=THEMES[theme_var.get()]["bg"], height=80)
    header_frame.pack(fill="x", padx=20, pady=15)
    
    global title_label
    title_label = Label(header_frame, text="🎬 YouTube Shorts İndirici Ultimate Pro", 
                       font=("Arial", 22, "bold"), 
                       bg=THEMES[theme_var.get()]["bg"], 
                       fg=THEMES[theme_var.get()]["accent"])
    title_label.pack(side="left")
    
    # Kontrol butonları
    control_frame = Frame(header_frame, bg=THEMES[theme_var.get()]["bg"])
    control_frame.pack(side="right")
    
    control_buttons = [
        ("⏸️", toggle_pause, "Duraklat/Devam Et"),
        ("📊", show_analytics, "Analiz"),
        ("🛠️", bulk_operations, "Toplu İşlemler"),
        ("💾", backup_data, "Yedekle"),
        ("🔍", advanced_search, "Gelişmiş Arama"),
        ("🌙", toggle_theme, "Tema Değiştir"),
        ("📖", show_instructions, "Talimatlar")
    ]
    
    for text, command, tooltip in control_buttons:
        btn = Button(control_frame, text=text, command=command,
                    bg=THEMES[theme_var.get()]["secondary"],
                    fg=THEMES[theme_var.get()]["fg"],
                    font=("Arial", 12),
                    width=3)
        btn.pack(side="left", padx=2)
    
    # Ana notebook
    global notebook
    notebook = Notebook(root)
    
    # Çerçeveleri oluştur
    frames = {}
    for tab_name in ["🚀 Kontrol Paneli", "📋 Kanallar", "🎬 Shorts", "📊 Analiz", "⚙️ Ayarlar", "📝 Loglar"]:
        frames[tab_name] = Frame(notebook)
        notebook.add(frames[tab_name], text=tab_name)
    
    notebook.pack(expand=True, fill="both", padx=10, pady=5)
    
    # Her sekmesi ayarla
    setup_dashboard_tab(frames["🚀 Kontrol Paneli"])
    setup_channels_tab(frames["📋 Kanallar"])
    setup_shorts_tab(frames["🎬 Shorts"])
    setup_analytics_tab(frames["📊 Analiz"])
    setup_settings_tab(frames["⚙️ Ayarlar"])
    setup_logs_tab(frames["📝 Loglar"])

def setup_dashboard_tab(frame):
    """Kontrol panelini widget'larla ayarla"""
    # Hızlı işlemler
    quick_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    quick_frame.pack(fill="x", padx=20, pady=10)
    
    quick_actions = [
        ("⚡ Hızlı Tarama", fetch_all_channels, THEMES[theme_var.get()]["accent"]),
        ("⬇️ Tümünü İndir", download_all_videos, "#4CAF50"),
        ("🔄 Tümünü Güncelle", update_all_channels, "#2196F3"),
        ("📊 Rapor Al", generate_report, "#FF9800")
    ]
    
    for text, command, color in quick_actions:
        btn = Button(quick_frame, text=text, command=command,
                    bg=color, fg="white", font=("Arial", 11, "bold"),
                    padx=20, pady=10)
        btn.pack(side="left", padx=10)
    
    # İstatistik genel bakış
    stats_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    stats_frame.pack(fill="x", padx=20, pady=20)
    
    # İlerleme
    global progress, status_label
    progress = Progressbar(frame, length=800, style="Horizontal.TProgressbar")
    progress.pack(pady=10)
    
    status_label = Label(frame, text="Sistem hazır - İşlemlerinizi başlatın", 
                        font=("Arial", 12), bg=THEMES[theme_var.get()]["bg"], 
                        fg=THEMES[theme_var.get()]["fg"])
    status_label.pack()

def setup_channels_tab(frame):
    """Kanallar sekmesini ayarla"""
    global channels_listbox
    
    # Kontroller
    controls_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    controls_frame.pack(fill="x", padx=20, pady=10)
    
    # Kanal girişi
    entry_frame = Frame(controls_frame, bg=THEMES[theme_var.get()]["bg"])
    entry_frame.pack(fill="x", pady=5)
    
    Label(entry_frame, text="Kanal URL:", bg=THEMES[theme_var.get()]["bg"], 
          fg=THEMES[theme_var.get()]["fg"]).pack(side="left")
    
    channel_entry = Entry(entry_frame, textvariable=channel_var, width=50)
    channel_entry.pack(side="left", padx=5)
    
    Button(entry_frame, text="Kanal Ekle", command=add_channel_manual,
           bg=THEMES[theme_var.get()]["accent"], fg=THEMES[theme_var.get()]["button_fg"]).pack(side="left", padx=5)
    
    # Dosya işlemleri
    file_frame = Frame(controls_frame, bg=THEMES[theme_var.get()]["bg"])
    file_frame.pack(fill="x", pady=5)
    
    Button(file_frame, text="TXT'den Yükle", command=load_channels_from_file,
           bg=THEMES[theme_var.get()]["secondary"], fg=THEMES[theme_var.get()]["fg"]).pack(side="left", padx=5)
    
    Button(file_frame, text="Seçileni Sil", command=remove_selected_channels,
           bg=THEMES[theme_var.get()]["error"], fg="white").pack(side="left", padx=5)
    
    Button(file_frame, text="Tüm Kanalları Getir", command=fetch_all_channels,
           bg=THEMES[theme_var.get()]["success"], fg="white").pack(side="left", padx=5)
    
    # Kanallar listbox'ı
    listbox_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    listbox_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    channels_listbox = Listbox(listbox_frame, selectmode=MULTIPLE, font=("Arial", 10))
    channels_listbox.pack(fill="both", expand=True)
    
    update_channels_listbox()

def setup_shorts_tab(frame):
    """Shorts sekmesini ayarla"""
    global canvas
    
    # Kontroller
    controls_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    controls_frame.pack(fill="x", padx=20, pady=10)
    
    Button(controls_frame, text="Seçileni İndir", command=download_selected_videos,
           bg=THEMES[theme_var.get()]["accent"], fg=THEMES[theme_var.get()]["button_fg"],
           font=("Arial", 11, "bold")).pack(side="left", padx=5)
    
    Button(controls_frame, text="Tümünü İndir", command=download_all_videos,
           bg=THEMES[theme_var.get()]["success"], fg="white",
           font=("Arial", 11, "bold")).pack(side="left", padx=5)
    
    # Shorts listesi için canvas
    canvas_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    canvas = Canvas(canvas_frame, bg=THEMES[theme_var.get()]["canvas_bg"])
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def setup_analytics_tab(frame):
    """Analiz sekmesini ayarla"""
    content_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    Label(content_frame, text="Analiz Paneli", font=("Arial", 16, "bold"),
          bg=THEMES[theme_var.get()]["bg"], fg=THEMES[theme_var.get()]["fg"]).pack(pady=10)
    
    Button(content_frame, text="Detaylı Analiz Göster", command=show_analytics,
           bg=THEMES[theme_var.get()]["accent"], fg=THEMES[theme_var.get()]["button_fg"]).pack(pady=10)

def setup_settings_tab(frame):
    """Ayarlar sekmesini ayarla"""
    content_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # İndirme klasörü
    folder_frame = Frame(content_frame, bg=THEMES[theme_var.get()]["bg"])
    folder_frame.pack(fill="x", pady=10)
    
    Label(folder_frame, text="İndirme Klasörü:", bg=THEMES[theme_var.get()]["bg"], 
          fg=THEMES[theme_var.get()]["fg"]).pack(anchor="w")
    
    folder_subframe = Frame(folder_frame, bg=THEMES[theme_var.get()]["bg"])
    folder_subframe.pack(fill="x", pady=5)
    
    folder_entry = Entry(folder_subframe, textvariable=folder_var, width=50)
    folder_entry.pack(side="left", fill="x", expand=True, padx=5)
    
    Button(folder_subframe, text="Gözat", command=select_folder,
           bg=THEMES[theme_var.get()]["secondary"], fg=THEMES[theme_var.get()]["fg"]).pack(side="right")
    
    # Kalite ayarları
    quality_frame = Frame(content_frame, bg=THEMES[theme_var.get()]["bg"])
    quality_frame.pack(fill="x", pady=10)
    
    Label(quality_frame, text="Video Kalitesi:", bg=THEMES[theme_var.get()]["bg"], 
          fg=THEMES[theme_var.get()]["fg"]).pack(anchor="w")
    
    quality_combo = Combobox(quality_frame, textvariable=quality_var, values=["720p", "1080p"], state="readonly")
    quality_combo.pack(fill="x", pady=5)
    
    # Ses ayarları
    audio_frame = Frame(content_frame, bg=THEMES[theme_var.get()]["bg"])
    audio_frame.pack(fill="x", pady=10)
    
    Checkbutton(audio_frame, text="Sesle İndir", variable=download_audio_var,
                style="TCheckbutton").pack(anchor="w")
    
    # Kaydet butonu
    Button(content_frame, text="Ayarları Kaydet", command=save_settings,
           bg=THEMES[theme_var.get()]["accent"], fg=THEMES[theme_var.get()]["button_fg"],
           font=("Arial", 11, "bold")).pack(pady=20)

def setup_logs_tab(frame):
    """Loglar sekmesini ayarla"""
    global log_area
    
    # Kontroller
    controls_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    controls_frame.pack(fill="x", padx=20, pady=10)
    
    Button(controls_frame, text="Logları Temizle", command=clear_log,
           bg=THEMES[theme_var.get()]["secondary"], fg=THEMES[theme_var.get()]["fg"]).pack(side="right")
    
    # Log alanı
    log_frame = Frame(frame, bg=THEMES[theme_var.get()]["bg"])
    log_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    log_area = Text(log_frame, wrap="word", font=("Consolas", 9))
    log_area.pack(fill="both", expand=True)

def select_folder():
    """İndirme klasörü seç"""
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)
        save_settings()
        log_area.insert(END, f"📁 İndirme klasörü ayarlandı: {folder}\n")

def clear_log():
    """Log alanını temizle"""
    if 'log_area' in globals():
        log_area.delete(1.0, END)
        log_area.insert(END, "Loglar temizlendi\n")

def toggle_pause():
    """Duraklatma durumunu değiştir"""
    global is_paused
    is_paused = not is_paused
    status_label.config(text="⏸️ Duraklatıldı" if is_paused else "▶️ Devam Ediyor")
    if 'log_area' in globals():
        log_area.insert(END, "⏸️ İndirmeler duraklatıldı\n" if is_paused else "▶️ İndirmeler devam ediyor\n")

# ----------------- Başlatma -----------------
def main():
    load_settings()
    create_main_gui()
    
    # Başlangıç mesajı
    if 'log_area' in globals():
        log_area.insert(END, "🚀 YouTube Shorts İndirici Ultimate Pro başlatıldı\n")
        log_area.insert(END, "📖 Talimatlar butonuna tıklayarak kullanım kılavuzunu okuyun\n\n")
    
    root.mainloop()

if __name__ == "__main__":
    main()
