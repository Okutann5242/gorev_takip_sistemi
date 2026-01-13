from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Category, Product


class Command(BaseCommand):
    help = "Demo kategoriler ve ürünler oluşturur (geliştirme için)."

    def handle(self, *args, **options):
        data = {
            "Elektronik": [
                ("Kablosuz Kulaklık", "Gün boyu konfor, güçlü bas ve net görüşme.", 899.90, 1199.90, 42, "PZ-EL-001"),
                ("Akıllı Saat", "Adım sayar, nabız takibi ve bildirim desteği.", 1299.00, 1599.00, 18, "PZ-EL-002"),
                ("Masaüstü Hoparlör", "Kompakt tasarım, güçlü stereo ses.", 749.50, None, 25, "PZ-EL-003"),
            ],
            "Ev & Yaşam": [
                ("Aromaterapi Difüzör", "Sessiz çalışma ve ayarlanabilir buhar modu.", 499.00, 649.00, 30, "PZ-EV-001"),
                ("Bambu Kesme Tahtası", "Dayanıklı, kolay temizlenir, şık görünüm.", 219.90, None, 60, "PZ-EV-002"),
                ("Akıllı Priz", "Zamanlama ve uzaktan kontrol özelliği.", 189.00, 249.00, 75, "PZ-EV-003"),
            ],
            "Moda": [
                ("Unisex Oversize Sweatshirt", "Yumuşak dokulu, günlük kullanım için ideal.", 649.00, 799.00, 40, "PZ-MD-001"),
                ("Spor Çanta", "Suya dayanıklı kumaş, geniş iç hacim.", 399.00, None, 22, "PZ-MD-002"),
                ("Güneş Gözlüğü", "UV400 koruma, hafif çerçeve.", 329.00, 449.00, 50, "PZ-MD-003"),
            ],
        }

        created_c = 0
        created_p = 0

        for cat_name, items in data.items():
            cat, created = Category.objects.get_or_create(
                slug=slugify(cat_name),
                defaults={"name": cat_name},
            )
            if not created:
                cat.name = cat_name
                cat.save()
            else:
                created_c += 1

            for name, short_desc, price, compare, stock, sku in items:
                p, p_created = Product.objects.get_or_create(
                    slug=slugify(f"{cat_name}-{name}")[:220],
                    defaults={
                        "category": cat,
                        "name": name,
                        "short_description": short_desc,
                        "description": short_desc + "\n\nDetaylar: Ürün sayfasındaki açıklamayı kendi ürününüzle değiştirin.",
                        "price": price,
                        "compare_at_price": compare,
                        "stock": stock,
                        "sku": sku,
                        "is_active": True,
                    },
                )
                if not p_created:
                    p.category = cat
                    p.name = name
                    p.short_description = short_desc
                    p.price = price
                    p.compare_at_price = compare
                    p.stock = stock
                    p.sku = sku
                    p.is_active = True
                    p.save()
                else:
                    created_p += 1

        self.stdout.write(self.style.SUCCESS(f"Tamamlandı. Yeni kategori: {created_c}, yeni ürün: {created_p}"))
