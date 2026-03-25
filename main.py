from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Veritabanı dosyası oluşturur
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aritma_isletme.db'
db = SQLAlchemy(app)

# --- VERİTABANI MODELLERİ ---

class Stok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parca_adi = db.Column(db.String(100), unique=True, nullable=False)
    adet = db.Column(db.Integer, default=0)

class Musteri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20))
    # Konum bilgisi (Enlem, Boylam)
    konum_lat = db.Column(db.Float)
    konum_lng = db.Column(db.Float)
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

# --- API ROTARI (İŞLEMLER) ---

# 1. ADMIN: STOK GÜNCELLEME
@app.route('/admin/stok_ekle', methods=['POST'])
def stok_ekle():
    data = request.json
    item = Stok.query.filter_by(parca_adi=data['parca_adi']).first()
    
    if item:
        item.adet = data['yeni_adet']
    else:
        item = Stok(parca_adi=data['parca_adi'], adet=data['yeni_adet'])
        db.session.add(item)
    
    db.session.commit()
    return jsonify({"mesaj": f"{item.parca_adi} stoğu güncellendi. Yeni adet: {item.adet}"})

# 2. PERSONEL: MÜŞTERİ VE KONUM KAYDI
@app.route('/personel/musteri_kaydet', methods=['POST'])
def musteri_kaydet():
    data = request.json
    yeni_musteri = Musteri(
        ad_soyad=data['ad_soyad'],
        telefon=data.get('telefon'),
        konum_lat=data['lat'], # Telefondan gelen GPS verisi
        konum_lng=data['lng']
    )
    db.session.add(yeni_musteri)
    db.session.commit()
    return jsonify({"mesaj": "Müşteri konumuyla birlikte kaydedildi!"})

# 3. GENEL: STOKLARI GÖRÜNTÜLE
@app.route('/stok_durumu', methods=['GET'])
def stok_durumu():
    stoklar = Stok.query.all()
    sonuc = {s.parca_adi: s.adet for s in stoklar}
    return jsonify(sonuc)

# Veritabanını oluştur ve başlat
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
