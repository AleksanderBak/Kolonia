from django.shortcuts import render
from .models import Pomieszczenia

# Create your views here.
def dashboard(request):
    # output = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(request, "dashboard.html")


def rooms(request):
    output = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(request, "rooms.html", {"Pomieszczenia": output})


def roomsNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        Pomieszczenia.objects.create(nazwa=name, opis=desc)
    return render(request, "rooms_new.html")


def roomsEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        id = request.POST["id"]
        Pomieszczenia.objects.filter(nr_pomieszczenia=id).update(nazwa=name, opis=desc)
    query = "SELECT * FROM pomieszczenia WHERE nr_pomieszczenia={id}".format(id=id)
    output = Pomieszczenia.objects.raw(query)[0]
    return render(request, "rooms_edit.html", {"Pomieszczenie": output})
