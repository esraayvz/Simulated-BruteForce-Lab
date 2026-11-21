#DOSYA: app.py (Backend Sunucusu)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#YASAL VE ETİK UYARI:
#- Bu yazılım ve içerdiği tüm simülasyon senaryoları tamamen EĞİTİM ve GELİŞTİRME amacıyla oluşturulmuştur. 
#- Tamamen yasal bir yerel test ortamında (localhost / 127.0.0.1) çalışmaktadır.
#- İçerisinde adı geçen 'Example Sample' ve tüm dossier (profil) verileri tamamen hayal ürünüdür; gerçek hayatta böyle bir kişi veya veri seti bulunmamaktadır.
#- Kötü niyetli kullanım veya yetkisiz sistemlere karşı test amacıyla KULLANILAMAZ. Tüm sorumluluk uygulayan kullanıcıya aittir.
#----------------------------------------------------------------------------------------------------------------------------------------------------------

from flask import Flask, render_template_string, request, jsonify
import bcrypt

app = Flask(__name__)

# --- OYUNUN GİZLİ HEDEF BİLGİLERİ ---
SECRET_EMAIL = "example@example.com"
RAW_PASSWORD = "matrix2026"  # Kırılacak orijinal gizli şifre

# Şifreyi açık metin yerine bcrypt ile güvenli bir şekilde hash'liyoruz
HASHED_PASSWORD = bcrypt.hashpw(RAW_PASSWORD.encode('utf-8'), bcrypt.gensalt())

# Hackleyeceğimiz hayali kişinin profil bilgileri (Veritabanı simülasyonu)
TARGET_DOSSIER = {
    "ad": "Example",
    "soyad": "Sample",
    "dogum_tarihi": "14.07.1998",
    "email": "example@example.com",
    "sifre": "matrix2026",
    "tc_no": "11111111111"
}

# 1. Normal login şablonu
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Secure Portal (CTF Lab)</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: #161b22; padding: 30px; border-radius: 8px; border: 1px solid #30363d; width: 320px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; text-align: center; margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-size: 14px; }
        input { width: 100%; padding: 10px; margin-bottom: 15px; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #238636; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        button:hover { background: #2ea043; }
        .error-box { background: rgba(255,51,51,0.1); border: 1px solid #ff3333; color: #ff6666; padding: 8px; text-align: center; font-size: 12px; border-radius: 4px; margin-bottom: 15px; }
        .footer { text-align: center; font-size: 11px; color: #8b949e; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔒 Üye Giriş Paneli</h2>
        
        {% if error %}
        <div class="error-box">{{ error }}</div>
        {% endif %}

        <form method="POST" action="/login">
            <label>E-posta Adresi:</label>
            <input type="email" name="email" required placeholder="example@example.com">
            <label>Şifre:</label>
            <input type="password" name="password" required placeholder="********">
            <button type="submit">Giriş Yap</button>
        </form>
        <div class="footer">Eğitim Amaçlı CTF Laboratuvarı</div>
    </div>
</body>
</html>
"""

# 2. Hayali kullanıcının kendisi normal bir şekilde login sayfasında mail ve şifresini girdiğinde karşısına çıkacak olan profil sayfası şablonu
NORMAL_PROFILE_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kullanıcı Paneli - Hoş Geldiniz</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #161b22; padding: 40px; border-radius: 8px; border: 1px solid #30363d; width: 420px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center; }
        h1 { color: #58a6ff; font-size: 20px; margin-bottom: 10px; }
        .welcome-msg { color: #238636; font-weight: bold; margin-bottom: 25px; font-size: 14px; }
        .info-row { display: flex; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #30363d; padding-bottom: 8px; font-size: 14px; text-align: left; }
        .label { color: #8b949e; }
        .value { color: #fff; }
        .logout-btn { display: inline-block; margin-top: 20px; padding: 8px 15px; background: #30363d; color: #c9d1d9; text-decoration: none; border-radius: 4px; font-size: 12px; }
        .logout-btn:hover { background: #484f58; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👤 Kullanıcı Portalı</h1>
        <div class="welcome-msg">Hoş geldin, Example Sample! Başarıyla giriş yaptın.</div>
        
        <div class="info-row"><span class="label">Ad Soyad:</span> <span class="value">{{ user.ad }} {{ user.soyad }}</span></div>
        <div class="info-row"><span class="label">E-posta:</span> <span class="value">{{ user.email }}</span></div>
        <div class="info-row"><span class="label">Doğum Tarihi:</span> <span class="value">{{ user.dogum_tarihi }}</span></div>
        <div class="info-row"><span class="label">TC Kimlik No:</span> <span class="value">{{ user.tc_no }}</span></div>

        <a href="/" class="logout-btn">Çıkış Yap</a>
    </div>
</body>
</html>
"""

# 3. Hackledikten sonra karşımıza çıkacak olan hesap kırıldı şablonu (Brute-Force Sonucu)
BREACH_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>HESAP ELE GEÇİRİLDİ - Veri Sızıntısı</title>
    <style>
        body { background-color: #05070b; color: #00ff66; font-family: 'Courier New', Courier, monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: #0d1117; padding: 40px; border-radius: 12px; border: 2px solid #00ff66; width: 450px; box-shadow: 0 0 25px rgba(0,255,102,0.3); }
        h1 { color: #ff3333; text-align: center; font-size: 22px; margin-bottom: 20px; letter-spacing: 2px; }
        .info-row { display: flex; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px dashed #30363d; padding-bottom: 8px; font-size: 15px; }
        .label { color: #8b949e; font-weight: bold; }
        .value { color: #c9d1d9; }
        .alert-box { background: rgba(255,51,51,0.1); border: 1px solid #ff3333; color: #ff6666; padding: 10px; text-align: center; font-size: 13px; border-radius: 6px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚠️ HESAP KIRILDI ⚠️</h1>
        <p style="text-align: center; color: #58a6ff; font-size: 13px; margin-bottom: 20px;">Brute-Force Simülasyonu Başarılı - Gizli Veriler Ele Geçirildi</p>
        
        <div class="info-row"><span class="label">Ad:</span> <span class="value">{{ dossier.ad }}</span></div>
        <div class="info-row"><span class="label">Soyad:</span> <span class="value">{{ dossier.soyad }}</span></div>
        <div class="info-row"><span class="label">Doğum Tarihi:</span> <span class="value">{{ dossier.dogum_tarihi }}</span></div>
        <div class="info-row"><span class="label">E-posta:</span> <span class="value">{{ dossier.email }}</span></div>
        <div class="info-row"><span class="label">Şifre (Cracked):</span> <span class="value" style="color:#00ff66;">{{ dossier.sifre }}</span></div>
        <div class="info-row"><span class="label">TC Kimlik No:</span> <span class="value">{{ dossier.tc_no }}</span></div>

        <div class="alert-box">GİZLİLİK UYARISI: Bu veriler yalnızca eğitim amaçlı simüle edilmiştir.</div>
    </div>
</body>
</html>
"""

# --- ANA UYGULAMA ROTLARI VE SUNUCU BAŞLANGICI ---

# 1. Ana Sayfa (Kök Dizin): Kullanıcı tarayıcıdan siteye ilk girdiğinde (GET isteği) bu fonksiyon çalışır ve "Üye Giriş Paneli" şablonunu ekrana getirir.
@app.route('/')
def home():
    return render_template_string(LOGIN_TEMPLATE)

# 2. Giriş İşlemi (Login Route): Kullanıcı form doldurup "Giriş Yap" butonuna bastığında (POST isteği) formdaki e-posta ve şifre verileri buraya gönderilir.
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # bcryptnin çalıştığını kanıtlar.
    print(f"[-] Denenen şifre bcrypt ile test ediliyor: {password}")

    # E-posta doğru mu VE kullanıcının girdiği şifre bcrypt ile hash'lenmiş şifreyle uyuşuyor mu?
    if email == SECRET_EMAIL and bcrypt.checkpw(password.encode('utf-8'), HASHED_PASSWORD):
        
        # Eğer istek saldırı aracından (JSON) geliyorsa verileri sızdırıyoruz.
        if request.headers.get('Accept') == 'application/json' or request.is_json:
            return jsonify({
                "status": "success",
                "message": "Password cracked successfully",
                "cracked_password": password,
                "dossier": TARGET_DOSSIER
            }), 200

        # Normal insan kullanıcı giriş yaptıysa profil sayfasını açıyoruz.
        return render_template_string(NORMAL_PROFILE_TEMPLATE, user=TARGET_DOSSIER), 200
    else:
        return render_template_string(LOGIN_TEMPLATE, error="Hatalı e-posta veya şifre!"), 401

# 3. Veri Sızıntısı / Breach Rotu: Arka plandaki sızma betiği şifreyi kırdığında tarayıcının otomatik açacağı "HESAP KIRILDI" veri sızıntısı ekranını yansıtır.
@app.route('/breach')
def breach():
    return render_template_string(BREACH_TEMPLATE, dossier=TARGET_DOSSIER)

# 4. Sunucuyu Başlatma Bloğu: Kod doğrudan çalıştırıldığında Flask web sunucusunu yerel bilgisayarımızda (127.0.0.1) ve 5000 numaralı port üzerinde ayağa kaldırır.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)