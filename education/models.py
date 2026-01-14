from django.db import models
from django.utils.text import slugify


class TrainingPDF(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    pdf = models.FileField(upload_to="education/pdfs/")
    order = models.PositiveIntegerField(default=0)
    is_activate = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
