from pathlib import Path

from django.core.files import File
from django.db import migrations


def seed_pdfs(apps, schema_editor):
    TrainingPDF = apps.get_model("education", "TrainingPDF")

    app_dir = Path(__file__).resolve().parent.parent
    seed_dir = app_dir / "seed_pdfs"
    if not seed_dir.exists():
        return

    # (title, slug, filename, order, description)
    items = [
        ("Python ile Uygulamalı Programlama (Tam Rehber)", "python-programlama", "python-programlama.pdf", 10, "Sıfırdan ileri seviyeye: temel kavramlar, OOP, dosya işlemleri, test yaklaşımı ve mini proje."),
        ("Django ile E‑Ticaret Uygulaması Geliştirme", "django-eticaret", "django-eticaret.pdf", 20, "Katalog, sepet, checkout, sipariş yönetimi, admin özelleştirme ve üretim notları."),
        ("Satış ve Dijital Pazarlama: Dönüşüm Odaklı Rehber", "dijital-pazarlama", "dijital-pazarlama.pdf", 30, "Konumlandırma, dönüşüm optimizasyonu, kampanya planlama, KPI ve A/B test yaklaşımı."),
        ("SEO ile Organik Trafik Artırma (Uygulamalı)", "seo-rehberi", "seo-rehberi.pdf", 40, "Teknik SEO, içerik planı, site mimarisi, CWV, schema ve raporlama adımları."),
        ("E‑Ticarette Müşteri Hizmetleri ve Operasyon", "operasyon-musteri-hizmetleri", "operasyon-musteri-hizmetleri.pdf", 50, "Kargo, iade, SLA, self-service, kalite ölçümü ve operasyonel kontrol listeleri."),
        ("Güvenlik ve Ödeme Sistemleri (Temel + Pratik)", "guvenlik-odeme", "guvenlik-odeme.pdf", 60, "OWASP özeti, CSRF/XSS/SQLi önlemleri, güvenli oturum, ödeme akışı tasarımı ve izleme/yedekleme."),
    ]

    for title, slug, filename, order, desc in items:
        obj, created = TrainingPDF.objects.get_or_create(
            slug=slug,
            defaults={"title": title, "order": order, "description": desc, "is_active": True},
        )

        if obj.pdf and obj.pdf.name:
            continue

        file_path = seed_dir / filename
        if not file_path.exists():
            continue

        with file_path.open("rb") as f:
            obj.pdf.save(filename, File(f), save=True)


class Migration(migrations.Migration):
    dependencies = [
        ("education", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_pdfs, migrations.RunPython.noop),
    ]
