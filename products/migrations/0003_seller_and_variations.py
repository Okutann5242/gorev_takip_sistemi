from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("products", "0002_product_upgrade_and_reviews"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="seller",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="ProductVariationType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="variation_types", to="products.product")),
                ("variation_type", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.variationtype")),
            ],
            options={"unique_together": {("product", "variation_type")}},
        ),
        migrations.CreateModel(
            name="ProductVariationOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("extra_price", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("option", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.variationoption")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="variation_options", to="products.product")),
            ],
            options={"unique_together": {("product", "option")}},
        ),
    ]
