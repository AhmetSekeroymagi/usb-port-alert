import wmi
import time
import sounddevice as sd
import numpy as np
# Yeni eklenen kütüphaneler
import cv2  # Kamera için (OpenCV)
import datetime # Dosya ismine tarih saat eklemek için
import os # Klasör oluşturmak için
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- YENİ FOTOĞRAF FONKSİYONU ---
def fotograf_cek():
    """
    USB çekildiği an çalışır. Kamerayı açar, tek bir kare fotoğraf çeker
    ve tarih-saat damgasıyla kaydeder.
    """
    print("\n📸 FOTOĞRAF ÇEKİLİYOR...")
    
    # 1. Kayıt klasörünü ayarla
    klasor_adi = "guvenlik_fotograflari"
    if not os.path.exists(klasor_adi):
        os.makedirs(klasor_adi)
        print(f"   -> '{klasor_adi}' klasörü oluşturuldu.")

    # 2. Dosya ismini oluştur (Tarih_Saat.jpg)
    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dosya_yolu = os.path.join(klasor_adi, f"ihlal_{zaman_damgasi}.jpg")

    # 3. Kamerayı başlat (0 genellikle varsayılan webcam'dir)
    # Windows'ta CAP_DSHOW bazen daha hızlı açılmasını sağlar
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ HATA: Kamera açılamadı! Başka bir program kullanıyor olabilir.")
        return

    # 4. Kameranın ışık ayarı yapması için birkaç 'ısınma' karesi oku
    # İlk kare genellikle çok karanlık olur.
    for _ in range(5):
        cap.read()

    # 5. Asıl fotoğrafı çek
    ret, frame = cap.read()

    if ret:
        # Fotoğraf başarılı çekildiyse kaydet
        cv2.imwrite(dosya_yolu, frame)
        print(f"✅ FOTOĞRAF KAYDEDİLDİ: {dosya_yolu}")
    else:
        print("❌ HATA: Görüntü alınamadı!")

    # 6. Kamerayı kapat ve serbest bırak
    cap.release()
# --------------------------------

def hoparlor_donanimini_bul():
    """ Doğru ses kartı ID'sini bulur (Realtek/Hoparlör öncelikli). """
    print("\n🔎 Ses Cihazları Taranıyor...")
    cihazlar = sd.query_devices()
    en_iyi_aday = None
    yedek_aday = None
    for i, cihaz in enumerate(cihazlar):
        if cihaz['max_output_channels'] > 0:
            ad = cihaz['name'].lower()
            if "kulaklık" in ad or "headphone" in ad or "usb" in ad: continue
            if "hoparlör" in ad and "realtek" in ad:
                en_iyi_aday = i
                break
            if "hoparlör" in ad and en_iyi_aday is None: en_iyi_aday = i
            if "speaker" in ad and yedek_aday is None: yedek_aday = i
    return en_iyi_aday if en_iyi_aday is not None else yedek_aday

def realtek_sesini_fulle():
    """ Hoparlör dahil tüm çıkışların sesini %100 yapar. """
    try:
        enumerator = AudioUtilities.GetDeviceEnumerator()
        collection = enumerator.EnumAudioEndpoints(0, 1)
        for i in range(collection.GetCount()):
            endpoint = collection.Item(i)
            try:
                interface = endpoint.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                if volume.GetMute() == 1: volume.SetMute(0, None)
                volume.SetMasterVolumeLevelScalar(1.0, None)
            except: continue
    except: pass

def ses_dalga_olustur(frekans, sure):
    """ Rahatsız edici kare dalga sesi """
    fs = 44100
    t = np.linspace(0, sure, int(fs * sure), endpoint=False)
    dalga = 0.5 * np.sign(np.sin(2 * np.pi * frekans * t))
    return dalga, fs

def alarm_cal(kayip_cihaz_bilgisi, hoparlor_id):
    isim, device_id = kayip_cihaz_bilgisi
    print(f"\n🚨 ALARM! CİHAZ KOPARILDI: {isim} 🚨")
    
    realtek_sesini_fulle()
    data, fs = ses_dalga_olustur(3000, 1.0)
    print(f"🔊 Ses ID {hoparlor_id} (Realtek Hoparlör) üzerinden çalınıyor...")

    for i in range(5):
        realtek_sesini_fulle()
        try:
            if hoparlor_id is not None:
                sd.play(data, fs, device=hoparlor_id)
            else:
                sd.play(data, fs)
            sd.wait()
        except Exception as e:
             time.sleep(1)

def cihazlari_getir(wmi_objesi):
    return set((d.Name, d.DeviceID) for d in wmi_objesi.Win32_PnPEntity() if d.Name and 'USB' in d.Name)

def main():
    print("-" * 60)
    print("🛡️  USB BEKÇİSİ (FOTOĞRAF + REALTEK HOPARLÖR MODU)")
    print("📷  Özellik: İhlal anında fotoğraf çeker.")
    print("🔊  Özellik: Sesi kulaklık takılı olsa bile HOPARLÖRDEN verir.")
    print("-" * 60)

    gercek_hoparlor_id = hoparlor_donanimini_bul()
    if gercek_hoparlor_id is not None:
        device_info = sd.query_devices(gercek_hoparlor_id)
        print(f"\n✅ HEDEF SES CİHAZI: {device_info['name']} (ID: {gercek_hoparlor_id})")
    else:
        print("\n❌ Hoparlör bulunamadı! Varsayılan cihaz kullanılacak.")

    c = wmi.WMI()
    guvenli_liste = cihazlari_getir(c)
    
    print(f"\n✅ KORUMA AKTİF! ({len(guvenli_liste)} cihaz izleniyor)")
    
    # Kamera testi yapalım
    print("\n📷 Kamera testi yapılıyor (Lütfen kameraya gülümseyin)...")
    fotograf_cek()
    print("(Test fotoğrafı 'guvenlik_fotograflari' klasörüne kaydedildi.)")

    print("\n(Program çalışıyor... Çıkmak için CTRL+C)")

    try:
        while True:
            simdiki_liste = cihazlari_getir(c)
            eksilenler = guvenli_liste - simdiki_liste

            if eksilenler:
                print("\n⚠️ İHLAL TESPİT EDİLDİ!")
                
                # 1. ÖNCE FOTOĞRAF ÇEK (Sessizce)
                fotograf_cek()
                
                # 2. SONRA ALARMI ÇAL
                for kayip in eksilenler:
                    alarm_cal(kayip, gercek_hoparlor_id)
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n👋 Sistem kapatıldı.")

if __name__ == "__main__":
    main()