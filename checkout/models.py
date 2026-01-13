from django.conf import settings
from django.db import models

from products.models import Product
from core.models import DiscountCode, ShippingMethod, VariationOption


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart({self.user_id})"

    @property
    def total_amount(self):
        return sum((item.line_total for item in self.items.all()), 0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def selected_options(self):
        return [link.option for link in self.option_links.select_related('option', 'option__variation_type')]

    def __str__(self) -> str:
        return f"{self.product} x{self.quantity}"

    @property
    def line_total(self):
        return self.product.price * self.quantity


class CartItemOption(models.Model):
    cart_item = models.ForeignKey("CartItem", on_delete=models.CASCADE, related_name="option_links")
    option = models.ForeignKey(VariationOption, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("cart_item", "option")

    def __str__(self) -> str:
        return f"{self.cart_item_id} -> {self.option}"


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=180)
    phone = models.CharField(max_length=30)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Adres"
        verbose_name_plural = "Adresler"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.city}/{self.district}"


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created", "Oluşturuldu"
        PAID = "paid", "Ödendi"
        SHIPPED = "shipped", "Kargoda"
        COMPLETED = "completed", "Tamamlandı"
        CANCELED = "canceled", "İptal"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order#{self.pk} ({self.get_status_display()})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    options_text = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.product} x{self.quantity}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
