from django.contrib import admin

from .models import TrainingPDF


@admin.register(TrainingPDF)
class TrainingPDFAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
