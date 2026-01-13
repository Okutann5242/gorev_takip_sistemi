from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from core.models import StoreProfile
from .forms import SignUpForm, VerifyCodeForm
from .models import UserProfile, VerificationCode


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"].strip().lower()
        user.is_active = False  # doğrulama sonrası aktif edeceğiz
        user.save()

        role = form.cleaned_data["role"]
        phone = (form.cleaned_data.get("phone") or "").strip()

        UserProfile.objects.create(user=user, role=role, phone=phone)

        if role == "seller":
            StoreProfile.objects.create(
                owner=user,
                store_name=form.cleaned_data["store_name"].strip(),
            )

        # Email doğrulama kodu
        if user.email:
            vc = VerificationCode.create_for(
                user=user,
                channel=VerificationCode.Channel.EMAIL,
                destination=user.email,
                minutes_valid=10,
            )

            send_mail(
                subject="Pazarcim doğrulama kodun",
                message=f"Doğrulama kodun: {vc.code} (10 dakika geçerli)",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@localhost"),
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session["verify_user_id"] = user.id
            messages.success(request, "Doğrulama kodu e-postana gönderildi.")
            return redirect("accounts:verify")

        # email yoksa aktif et (edge case)
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Hesabınız oluşturuldu.")
        return redirect("core:home")

    return render(request, "accounts/register.html", {"form": form})


def verify(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        return redirect("accounts:register")

    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.pop("verify_user_id", None)
        return redirect("accounts:register")

    form = VerifyCodeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        code = form.cleaned_data["code"].strip()

        vc = (
            VerificationCode.objects.filter(
                user=user,
                channel=VerificationCode.Channel.EMAIL,
                is_used=False,
            )
            .order_by("-created_at")
            .first()
        )

        if (not vc) or vc.is_expired() or vc.code != code:
            form.add_error("code", "Kod hatalı veya süresi dolmuş.")
        else:
            vc.is_used = True
            vc.save(update_fields=["is_used"])

            user.is_active = True
            user.save(update_fields=["is_active"])

            # profile flag
            if hasattr(user, "profile"):
                user.profile.email_verified = True
                user.profile.save(update_fields=["email_verified"])

            request.session.pop("verify_user_id", None)
            messages.success(request, "Hesabın doğrulandı. Giriş yapabilirsin.")
            return redirect("accounts:login")

    return render(request, "accounts/verify.html", {"form": form, "email": user.email})


def resend_verification(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        return redirect("accounts:register")

    user = User.objects.filter(id=user_id).first()
    if not user:
        request.session.pop("verify_user_id", None)
        return redirect("accounts:register")

    # basit rate limit: son 60 saniyede gönderildiyse engelle
    last = (
        VerificationCode.objects.filter(
            user=user, channel=VerificationCode.Channel.EMAIL
        )
        .order_by("-created_at")
        .first()
    )
    if last and (timezone.now() - last.created_at).total_seconds() < 60:
        messages.warning(request, "Lütfen yeniden göndermek için 1 dakika bekleyin.")
        return redirect("accounts:verify")

    vc = VerificationCode.create_for(
        user=user,
        channel=VerificationCode.Channel.EMAIL,
        destination=user.email,
        minutes_valid=10,
    )
    send_mail(
        subject="Pazarcim doğrulama kodun (yeniden)",
        message=f"Doğrulama kodun: {vc.code} (10 dakika geçerli)",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@localhost"),
        recipient_list=[user.email],
        fail_silently=False,
    )
    messages.success(request, "Yeni doğrulama kodu gönderildi.")
    return redirect("accounts:verify")


@login_required
def dashboard(request):
    profile = getattr(request.user, "profile", None)
    store = None
    if profile and profile.role == UserProfile.Role.SELLER:
        store = StoreProfile.objects.filter(owner=request.user).first()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "profile": profile,
            "store": store,
        },
    )
