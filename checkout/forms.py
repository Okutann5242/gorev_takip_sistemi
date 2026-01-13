from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "line1",
            "line2",
            "city",
            "district",
            "postal_code",
        ]
        widgets = {
            "line2": forms.TextInput(attrs={"placeholder": "(Opsiyonel)"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "(Opsiyonel)"}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "input")


class CheckoutExtrasForm(forms.Form):
    discount_code = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "İndirim kodu"}),
    )
