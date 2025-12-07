from django.shortcuts import render
#Güncelleme
def login_view(request):
    return render(request, "accounts/login.html")

def register_view(request):
    return render(request, "accounts/register.html")

def dashboard(request):
    return render(request, "accounts/dashboard.html")
from django.shortcuts import render, redirect

# Dummy fake database (models kullanılmıyor)
FAKE_USERS = ["test@mail.com", "demo@mail.com"]

def login_page(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email not in FAKE_USERS or password != "12345":
            error = "E-posta veya şifre hatalı!"
        else:
            return redirect("accounts:dashboard")

    return render(request, "accounts/login.html", {"error": error})


def register(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email in FAKE_USERS:
            error = "Bu e-posta zaten kayıtlı!"
        elif username.lower() == "demo":
            error = "Bu kullanıcı adı kullanılıyor!"
        else:
            FAKE_USERS.append(email)
            return redirect("accounts:login")

    return render(request, "accounts/register.html", {"error": error})


def dashboard(request):
    return render(request, "accounts/dashboard.html")
