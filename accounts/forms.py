from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

AUTH_INPUT_ATTRS = {
    "class": "auth-input",
    "autocomplete": "off",
}

ROLE_CHOICES = (
    ("buyer", "Sadece Alıcıyım"),
    ("seller", "Satıcı Olacağım"),
)


class LoginForm(AuthenticationForm):
    """Styled via our auth-input class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("username", "password"):
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(AUTH_INPUT_ATTRS)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)
    store_name = forms.CharField(required=False, max_length=150, label="Dükkan adı")
    phone = forms.CharField(required=False, max_length=32, label="Telefon (opsiyonel)")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "store_name", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in self.fields:
            if name == "role":
                continue
            self.fields[name].widget.attrs.update(AUTH_INPUT_ATTRS)

        self.fields["role"].widget.attrs.update({"class": "auth-radio"})

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu e-posta zaten kayıtlı.")
        return email

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        store_name = (cleaned.get("store_name") or "").strip()
        if role == "seller" and not store_name:
            self.add_error("store_name", "Satıcı kaydı için dükkan adı zorunludur.")
        return cleaned


class VerifyCodeForm(forms.Form):
    code = forms.CharField(min_length=6, max_length=6, label="Doğrulama kodu")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["code"].widget.attrs.update(AUTH_INPUT_ATTRS)
        self.fields["code"].widget.attrs.update({"inputmode": "numeric", "pattern": "[0-9]*"})
