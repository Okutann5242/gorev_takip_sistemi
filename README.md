# Pazarcim (Django)

Pazarcim; ürün kataloğu, sepet/checkout, sipariş yönetimi ve satıcı paneli içeren **e-ticaret prototipi** + satıcılara yönelik **tam içerikli eğitim modülü** içeren bir Django projesidir.

## Özellikler

### E-Ticaret
- Ürün kataloğu (arama + kategori filtre)
- Ürün detay (görsel, stok, fiyat, yorumlar)
- Sepet ve sipariş akışı (demo ödeme)
- Satıcı paneli (temel): ürün ekleme ve ürün listeleme
- Django Admin yönetimi

### Eğitimler
- Eğitim listesi + eğitim detay (modül/ders yapısı)
- Kullanıcı girişine göre “eğitime kaydol” akışı
- Admin panelinden eğitim/modül/ders yönetimi
- **Seed komutu ile 6 eğitim / çok sayıda ders** (örnek değil, tam içerik)

## Kurulum

Python 3.10+ önerilir.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Uygulama: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/

## Demo veri (opsiyonel ama önerilir)

```bash
# Demo ürün/kategori
python manage.py seed_shop

# Tam içerikli eğitim verisi
python manage.py # seed_trainings removed - pdfs are seeded via migration
```

## Notlar
- Ödeme ekranı demo amaçlıdır; gerçek ödeme sağlayıcı entegrasyonu yoktur.
- Ürün görseli yüklemek için Pillow bağımlılığı kullanılır.
