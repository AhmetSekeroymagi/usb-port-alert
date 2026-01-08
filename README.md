# 🛡️ USB Port Watchdog (Anti-Theft Alarm)

Bu proje, bilgisayarınıza bağlı USB cihazlarını korumak için geliştirilmiş, Python tabanlı gelişmiş bir güvenlik sistemidir. Bir USB cihazı (Mouse, Klavye, Flash Bellek vb.) izinsiz çekildiği anda devreye girer, saldırganın fotoğrafını çeker ve kulaklık takılı olsa bile bilgisayarın dahili hoparlörlerinden yüksek sesli alarm çalar.

## 🚀 Özellikler

* **📸 Anlık İhlal Fotoğrafı:** USB çekildiği anda webcam üzerinden sessizce fotoğraf çeker ve tarih/saat damgasıyla kaydeder.
* **🔊 Akıllı Ses Yönlendirme:** Bilgisayarda kulaklık takılı olsa bile, yazılım bunu algılar ve alarm sesini zorla **Hoparlör (Realtek/Speaker)** çıkışına yönlendirir.
* **📢 Mute Override (Sessiz Modu Aşma):** Bilgisayarın sesi kapalı (Mute) veya kısık olsa bile, alarm anında sesi açar ve %100 seviyesine getirir.
* **🔒 Snapshot Yöntemi:** Program başladığı anda takılı olan cihazları "Güvenli Liste" olarak kabul eder. Ekstra konfigürasyon gerektirmez.
* **🆔 Benzersiz ID Kontrolü:** Sadece cihaz ismine değil, donanım kimliğine (Hardware ID) bakar. Aynı marka/model iki cihazınız olsa bile hangisinin çekildiğini ayırt eder.

## 🛠️ Kullanılan Teknolojiler

Bu proje aşağıdaki Python kütüphanelerinden güç alır:

* **OpenCV (`cv2`):** Görüntü yakalama ve kaydetme işlemleri için.
* **SoundDevice & Numpy:** Özel frekanslı rahatsız edici alarm sesi (Square Wave) üretmek ve ses kartı yönetimi için.
* **Pycaw (Core Audio Windows):** Windows ses düzeyini (Master Volume) kontrol etmek ve sessiz moddan çıkarmak için.
* **WMI:** Windows donanım değişikliklerini anlık izlemek için.

## 📦 Kurulum

Projeyi bilgisayarınıza klonlayın ve gerekli kütüphaneleri yükleyin:

```bash
git clone [https://github.com/AhmetSekeroymagi/usb-port-alert.git](https://github.com/AhmetSekeroymagi/usb-port-alert.git)
cd usb-port-alert
pip install -r requirements.txt
