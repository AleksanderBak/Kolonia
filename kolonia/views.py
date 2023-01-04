from django.shortcuts import render
from .models import Pomieszczenia

# Create your views here.
def dashboard(request):
    output = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(request, "dashboard.html", {"Pomieszczenia": output})
