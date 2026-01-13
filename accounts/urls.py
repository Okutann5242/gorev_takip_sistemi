from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    path(
        "giris/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("cikis/", auth_views.LogoutView.as_view(), name="logout"),
    path("kayit/", views.register, name="register"),
    path("dogrula/", views.verify, name="verify"),
    path("dogrula/yeniden-gonder/", views.resend_verification, name="resend_verification"),
    path("panel/", views.dashboard, name="dashboard"),
]
