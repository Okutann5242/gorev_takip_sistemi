from django.urls import path
from . import views

app_name = "checkout"

urlpatterns = [
    path("sepet/", views.cart_detail, name="cart"),
    path("sepet/ekle/<int:product_id>/", views.cart_add, name="cart_add"),
    path("sepet/sil/<int:item_id>/", views.cart_remove, name="cart_remove"),

    path("", views.checkout, name="checkout"),
    path("odeme/<int:order_id>/", views.payment, name="payment"),
    path("basarili/<int:order_id>/", views.success, name="success"),

    path("adresler/", views.addresses, name="addresses"),
    path("adres/yeni/", views.address_new, name="address_new"),
    path("adres/<int:pk>/duzenle/", views.address_edit, name="address_edit"),
    path("adres/<int:pk>/sil/", views.address_delete, name="address_delete"),
    path("siparislerim/", views.my_orders, name="my_orders"),
]
