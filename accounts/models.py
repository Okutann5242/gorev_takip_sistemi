from __future__ import annotations

import random
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    class Role(models.TextChoices):
        BUYER = "buyer", "Alıcı"
        SELLER = "seller", "Satıcı"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    phone = models.CharField(max_length=32, blank=True)

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user_id} - {self.role}"


class VerificationCode(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="verification_codes"
    )
    channel = models.CharField(max_length=10, choices=Channel.choices)
    destination = models.CharField(max_length=255)
    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user", "channel", "is_used", "-created_at"]),
        ]

    @staticmethod
    def generate_code() -> str:
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_for(cls, *, user, channel: str, destination: str, minutes_valid: int = 10) -> "VerificationCode":
        return cls.objects.create(
            user=user,
            channel=channel,
            destination=destination,
            code=cls.generate_code(),
            expires_at=timezone.now() + timedelta(minutes=minutes_valid),
        )

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at
