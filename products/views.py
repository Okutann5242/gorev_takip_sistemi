from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ReviewForm
from .models import Category, Product, Review, ProductVariationType, ProductVariationOption


def product_list(request):
    """Katalog sayfası: arama + kategori filtre."""
    q = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    products_qs = Product.objects.filter(is_active=True).select_related("category")
    if q:
        products_qs = products_qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "products/list.html",
        {
            "items": products_qs,
            "categories": categories,
            "q": q,
            "category_slug": category_slug,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("reviews__user"),
        slug=slug,
        is_active=True,
    )
    reviews = product.reviews.filter(is_approved=True)

    form = None
    if request.user.is_authenticated:
        form = ReviewForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "comment": form.cleaned_data["comment"],
                    "is_approved": True,
                },
            )
            messages.success(request, "Yorumunuz kaydedildi. Teşekkürler.")
            return redirect(reverse("products:detail", kwargs={"slug": product.slug}))

    return render(
        request,
        "products/detail.html",
        {"item": product, "reviews": reviews, "review_form": form, "variation_types": ProductVariationType.objects.filter(product=product).select_related("variation_type"), "variation_options": ProductVariationOption.objects.filter(product=product).select_related("option", "option__variation_type")},
    )
