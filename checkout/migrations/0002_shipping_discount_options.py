from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_storeprofile_slug"),
        ("checkout", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CartItemOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cart_item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="option_links", to="checkout.cartitem")),
                ("option", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.variationoption")),
            ],
            options={"unique_together": {("cart_item", "option")}},
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_method",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.shippingmethod"),
        ),
        migrations.AddField(
            model_name="order",
            name="shipping_fee",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_code",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.discountcode"),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="order",
            name="subtotal_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="options_text",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
