import cv2
import time
import os
import glob
import requests
from dotenv import load_dotenv 

load_dotenv() 


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


KULLANICI_PROFILI = os.environ.get("USERPROFILE") or os.path.expanduser("~")
MASAUSTU_YOLU = os.path.join(KULLANICI_PROFILI, "Desktop")
KAYIT_KLASORU = os.path.join(MASAUSTU_YOLU, "kamera_kayitlari")

if not os.path.exists(KAYIT_KLASORU):
    os.makedirs(KAYIT_KLASORU)

def telefona_mesaj_gonder(mesaj):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mesaj})
    except: pass

def telefona_video_gonder(video_yolu):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    try:
        with open(video_yolu, 'rb') as video:
            requests.post(url, files={'video': video}, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': "1 dakikalık kayıt."})
    except: pass

def eski_videolari_temizle():
    videolar = glob.glob(os.path.join(KAYIT_KLASORU, "*.mp4"))
    if len(videolar) >= 10:
        videolar.sort(key=os.path.getmtime)
        while len(videolar) >= 10:
            try: os.remove(videolar.pop(0))
            except: pass

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2) 

ilk_kare = None
kayit_yapiliyor = False
kayit_baslangic_suresi = 0
video_yazici = None
KAYIT_SURESI_SANIYE = 60  
mevcut_video_adi = ""

telefona_mesaj_gonder("Kamera sistemi aktif! 🚨")

try:
    while True:
        ret, kare = cap.read()
        if not ret: break
        gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        gri = cv2.GaussianBlur(gri, (21, 21), 0)
        if ilk_kare is None:
            ilk_kare = gri
            continue
        kare_farki = cv2.absdiff(ilk_kare, gri)
        esik_deger = cv2.threshold(kare_farki, 25, 255, cv2.THRESH_BINARY)[1]
        esik_deger = cv2.dilate(esik_deger, None, iterations=2)
        konturlar, _ = cv2.findContours(esik_deger.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hareket_var = False
        for kontur in konturlar:
            if cv2.contourArea(kontur) < 5000: continue
            hareket_var = True
            break
        su_an = time.time()
        if hareket_var and not kayit_yapiliyor:
            eski_videolari_temizle()
            telefona_mesaj_gonder("⚠️ Kamerada hareket algılandı!")
            kayit_yapiliyor = True
            kayit_baslangic_suresi = su_an
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            mevcut_video_adi = os.path.join(KAYIT_KLASORU, f"kayit_{int(su_an)}.mp4")
            genislik = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) if cv2.CAP_PROP_FRAME_WIDTH else 640)
            yukseklik = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) if cv2.CAP_PROP_FRAME_HEIGHT else 480)
            video_yazici = cv2.VideoWriter(mevcut_video_adi, fourcc, 20.0, (genislik, yukseklik))
        if kayit_yapiliyor:
            video_yazici.write(kare)
            if su_an - kayit_baslangic_suresi >= KAYIT_SURESI_SANIYE:
                kayit_yapiliyor = False
                video_yazici.release()
                ilk_kare = None  
                telefona_video_gonder(mevcut_video_adi)
        if not kayit_yapiliyor and int(su_an) % 10 == 0: ilk_kare = gri
        time.sleep(0.05)
except KeyboardInterrupt: pass
finally:
    if video_yazici is not None: video_yazici.release()
    cap.release()
    cv2.destroyAllWindows()