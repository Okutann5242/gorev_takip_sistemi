from django import forms

from .models import Product, Review


INPUT_ATTRS = {"class": "input"}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "description",
            "sku",
            "price",
            "compare_at_price",
            "stock",
            "is_active",
            "image",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"class": "input", "rows": 6}),
            "short_description": forms.Textarea(attrs={"class": "input", "rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if isinstance(f.widget, forms.widgets.Textarea):
                continue
            f.widget.attrs.update(INPUT_ATTRS)
        # Ensure textareas have class too
        for name in ("description", "short_description"):
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "input")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={"class": "input"}),
            "comment": forms.Textarea(attrs={"class": "input", "rows": 4, "placeholder": "Deneyiminizi yazın..."}),
        }
