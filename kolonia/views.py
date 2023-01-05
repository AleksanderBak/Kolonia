from django.shortcuts import render
from django.db import connections
from .models import Pomieszczenia, Zasoby, Zawartosci, Systemy

# Create your views here.
def dashboard(request):
    # output = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(request, "dashboard.html")


def rooms(request):
    if request.method == "POST":
        id = request.POST["id"]
        Pomieszczenia.objects.get(nr_pomieszczenia=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM pomieszczenia WHERE UPPER(nr_pomieszczenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%';"""
        output = Pomieszczenia.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase)
        )
        return render(request, "rooms.html", {"Pomieszczenia": output})

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


def resources(request):
    if request.method == "POST":
        id = request.POST["id"]
        Zasoby.objects.get(nazwa=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        output = Zasoby.objects.filter(nazwa__icontains=phrase)
        return render(request, "resources.html", {"Zasoby": output})

    output = Zasoby.objects.raw("SELECT * FROM zasoby")
    return render(request, "resources.html", {"Zasoby": output})


def resourcesNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        Zasoby.objects.create(nazwa=name)
    return render(request, "resources_new.html")


def resourcesEdit(request, nazwa):
    name = ""
    if request.method == "POST":
        name = request.POST["nazwa"]
        Zasoby.objects.filter(nazwa=nazwa).update(nazwa=name)
    if name != "":
        output = Zasoby.objects.filter(nazwa=name)[0]
    else:
        output = Zasoby.objects.filter(nazwa=nazwa)[0]

    return render(request, "resources_edit.html", {"z": output})


def roomRes(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        query = "DELETE FROM zawartosci WHERE nazwa = '{name}' and nr_pomieszczenia = {id}".format(
            name=name, id=id
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM zawartosci WHERE UPPER(nr_pomieszczenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(liczba) like '%%{a3}%%' or UPPER(jednostka) like '%%{a4}%%';"""
        output = Zawartosci.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "room_res.html", {"Zawartosci": output})

    output = Zawartosci.objects.raw("SELECT * FROM zawartosci")
    return render(request, "room_res.html", {"Zawartosci": output})


def roomResNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        id = request.POST["nr_pomieszczenia"]
        quantity = request.POST["liczba"]
        unit = request.POST["jednostka"]
        query = "INSERT INTO zawartosci(nazwa, nr_pomieszczenia, liczba, jednostka) VALUES('{name}',{id},{quantity},'{unit}')".format(
            name=name, id=id, quantity=quantity, unit=unit
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        # Zawartosci.objects.create(
        #     nazwa=name, nr_pomieszczenia=id, liczba=quantity, jednostka=unit
        # )
    zasoby = Zasoby.objects.raw("SELECT * FROM zasoby")
    pomieszczenia = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(
        request, "room_res_new.html", {"Zasoby": zasoby, "Pomieszczenia": pomieszczenia}
    )


def roomResEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        id = request.POST["id"]
        Pomieszczenia.objects.filter(nr_pomieszczenia=id).update(nazwa=name, opis=desc)
    query = "SELECT * FROM pomieszczenia WHERE nr_pomieszczenia={id}".format(id=id)
    output = Pomieszczenia.objects.raw(query)[0]
    return render(request, "room_res_edit.html", {"Pomieszczenie": output})


def systems(request):
    if request.method == "POST":
        id = request.POST["id"]
        Systemy.objects.get(id_systemu=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM systemy WHERE id_systemu like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%';"""
        output = Systemy.objects.raw(query.format(a1=phrase, a2=phrase, a3=phrase))
        return render(request, "systems.html", {"Systemy": output})

    output = Systemy.objects.raw("SELECT * FROM systemy")
    return render(request, "systems.html", {"Systemy": output})


def systemsNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        Systemy.objects.create(nazwa=name, opis=desc)
    return render(request, "systems_new.html")


def systemsEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        Systemy.objects.filter(id_systemu=id).update(nazwa=name, opis=desc)
    query = "SELECT * FROM systemy WHERE id_systemu={id}".format(id=id)
    output = Systemy.objects.raw(query)[0]
    return render(request, "systems_edit.html", {"System": output})
