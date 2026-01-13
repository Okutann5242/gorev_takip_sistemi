from django.conf import settings
from django.db import models

from core.models import VariationType, VariationOption


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products", null=True, blank=True)
    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=220, unique=True)
    short_description = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)

    sku = models.CharField(max_length=60, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    image = models.ImageField(upload_to="products/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    @property
    def effective_price(self):
        return self.price

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def average_rating(self):
        qs = self.reviews.filter(is_approved=True)
        if not qs.exists():
            return 0
        return round(qs.aggregate(models.Avg("rating"))["rating__avg"] or 0, 1)

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductVariationType(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variation_types")
    variation_type = models.ForeignKey(VariationType, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("product", "variation_type")

    def __str__(self) -> str:
        return f"{self.product} / {self.variation_type}"


class ProductVariationOption(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="variation_options")
    option = models.ForeignKey(VariationOption, on_delete=models.PROTECT)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("product", "option")

    def __str__(self) -> str:
        return f"{self.product} / {self.option}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product} - {self.user} ({self.rating})"
