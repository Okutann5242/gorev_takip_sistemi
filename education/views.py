from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import TrainingPDF


def training_list(request):
    trainings = TrainingPDF.objects.filter(is_active=True).order_by("order", "title")
    return render(request, "education/training_list.html", {"trainings": trainings})


@login_required
def training_detail(request, slug: str):
    training = get_object_or_404(TrainingPDF, slug=slug, is_active=True)
    return render(request, "education/training_detail.html", {"training": training})
