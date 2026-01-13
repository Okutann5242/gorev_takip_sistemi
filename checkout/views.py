from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from core.models import DiscountCode, ShippingMethod

from products.models import Product, ProductVariationOption

from .forms import AddressForm, CheckoutExtrasForm
from .models import Address, Cart, CartItem, CartItemOption, Order, OrderItem


def _get_or_create_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = _get_or_create_cart(request.user)
    return render(request, "checkout/cart.html", {"cart": cart})


@login_required
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    option_ids = request.POST.getlist("option_ids")
    if option_ids:
        item.option_links.all().delete()
        for oid in option_ids:
            if str(oid).isdigit():
                CartItemOption.objects.get_or_create(cart_item=item, option_id=int(oid))

    if not created and not option_ids:
        item.quantity += 1
        item.save(update_fields=["quantity"])

    messages.success(request, "Ürün sepete eklendi.")
    return redirect(request.META.get("HTTP_REFERER", "products:list"))


@login_required
def cart_remove(request, item_id: int):
    cart = _get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, "Ürün sepetten çıkarıldı.")
    return redirect("checkout:cart")


@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)
    if cart.items.count() == 0:
        messages.warning(request, "Sepetiniz boş.")
        return redirect("products:list")

    shipping_methods = ShippingMethod.objects.filter(is_active=True).order_by("name")
    addresses = Address.objects.filter(user=request.user).order_by("-created_at")
    form = AddressForm(request.POST or None)
    extras_form = CheckoutExtrasForm(request.POST or None)

    if request.method == "POST":
        use_address_id = request.POST.get("use_address_id")
        if use_address_id:
            address = get_object_or_404(Address, id=use_address_id, user=request.user)
        else:
            if not form.is_valid():
                messages.error(request, "Adres bilgilerini kontrol edin.")
                return render(
                    request,
                    "checkout/checkout.html",
                    {"cart": cart, "form": form, "addresses": addresses, "shipping_methods": shipping_methods, "extras_form": extras_form},
                )
            address = form.save(commit=False)
            address.user = request.user
            address.save()

        discount = None
        code = (request.POST.get("discount_code") or "").strip()
        if code:
            discount = DiscountCode.objects.filter(code__iexact=code, is_active=True).first()
            if not discount:
                messages.error(request, "İndirim kodu geçersiz.")
                discount = None

        shipping_method = None
        shipping_id = request.POST.get("shipping_method_id")
        if shipping_id and str(shipping_id).isdigit():
            shipping_method = ShippingMethod.objects.filter(id=int(shipping_id), is_active=True).first()

        order = _create_order_from_cart(request.user, cart, address, discount=discount, shipping_method=shipping_method)
        messages.success(request, f"Sipariş oluşturuldu: #{order.id}")
        return redirect("checkout:payment", order_id=order.id)

    return render(
        request,
        "checkout/checkout.html",
        {"cart": cart, "form": form, "addresses": addresses, "shipping_methods": shipping_methods, "extras_form": extras_form},
    )
    address = form.save(commit=False)
    address.user = request.user
    address.save()

    order = _create_order_from_cart(user=request.user, cart=cart, address=address)
    messages.success(request, f"Sipariş oluşturuldu: #{order.id}")
    return redirect("checkout:payment", order_id=order.id)

    return render(
        request,
        "checkout/checkout.html",
        {"cart": cart, "form": form, "addresses": addresses},
    )


@transaction.atomic
def _create_order_from_cart(user, cart: Cart, address: Address, discount=None, shipping_method=None) -> Order:
    order = Order.objects.create(
        user=user,
        address=address,
        status=Order.Status.CREATED,
        discount_code=discount if discount else None,
        shipping_method=shipping_method if shipping_method else None,
        shipping_fee=(shipping_method.flat_fee if shipping_method else 0),
    )

    subtotal = 0
    for item in cart.items.select_related("product").prefetch_related("option_links__option"):
        extra = 0
        options = []
        for opt in item.selected_options:
            options.append(f"{opt.variation_type.name}: {opt.name}")
            pvo = ProductVariationOption.objects.filter(product=item.product, option=opt).first()
            if pvo:
                extra += pvo.extra_price

        unit = item.product.price + extra
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=unit,
            options_text=", ".join(options),
        )
        subtotal += unit * item.quantity

    discount_amount = 0
    if discount:
        discount_amount = (subtotal * discount.percent) / 100

    total = subtotal - discount_amount + order.shipping_fee
    if total < 0:
        total = 0

    order.subtotal_amount = subtotal
    order.discount_amount = discount_amount
    order.total_amount = total
    order.save(update_fields=["subtotal_amount", "discount_amount", "total_amount"])

    cart.items.all().delete()
    return order


@login_required
def payment(request, order_id: int):
    """Demo ödeme ekranı: gerçek ödeme entegrasyonu yok."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        order.status = Order.Status.PAID
        order.save(update_fields=["status"])
        messages.success(request, "Ödeme alındı (demo).")
        return redirect("checkout:success", order_id=order.id)

    return render(request, "checkout/payment.html", {"order": order})


@login_required
def success(request, order_id: int):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "checkout/success.html", {"order": order})


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    return render(request, "checkout/my_orders.html", {"orders": orders})

@login_required
def addresses(request):
    items = Address.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "checkout/addresses.html", {"addresses": items})


@login_required
def address_new(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        messages.success(request, "Adres eklendi.")
        return redirect("checkout:addresses")
    return render(request, "checkout/address_form.html", {"form": form, "mode": "create"})


@login_required
def address_edit(request, pk: int):
    obj = get_object_or_404(Address, pk=pk, user=request.user)
    form = AddressForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Adres güncellendi.")
        return redirect("checkout:addresses")
    return render(request, "checkout/address_form.html", {"form": form, "mode": "edit", "address": obj})


@login_required
def address_delete(request, pk: int):
    obj = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Adres silindi.")
        return redirect("checkout:addresses")
    return render(request, "checkout/address_delete_confirm.html", {"address": obj})
