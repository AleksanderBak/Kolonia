from django.shortcuts import render
from django.db import connections
from .models import (
    Pomieszczenia,
    Zasoby,
    Zawartosci,
    Systemy,
    PomieszczeniaSystemy,
    Badania,
)

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
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM zawartosci WHERE UPPER(nr_pomieszczenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(liczba) like '%%{a3}%%' or UPPER(jednostka) like '%%{a4}%%';"""
        output = Zawartosci.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "room_res.html", {"Zawartosci": output})

    output = Zawartosci.objects.raw(
        "SELECT z.*, p.nazwa AS nazwa_pom FROM zawartosci z INNER JOIN pomieszczenia p on z.nr_pomieszczenia = p.nr_pomieszczenia"
    )
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
    zasoby = Zasoby.objects.raw("SELECT * FROM zasoby")
    pomieszczenia = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(
        request, "room_res_new.html", {"Zasoby": zasoby, "Pomieszczenia": pomieszczenia}
    )


def roomResEdit(request, id):
    id_pom = int(id.split(".")[0])
    zasob = id.split(".")[1]

    if request.method == "POST":
        new_id_pom = request.POST["id_pom"]
        new_zasob = request.POST["zasob"]
        liczba = request.POST["liczba"]
        jednostka = request.POST["jednostka"]
        query_delete = "DELETE FROM zawartosci WHERE nazwa = '{name}' and nr_pomieszczenia = {id}".format(
            name=zasob, id=id_pom
        )

        query_insert = "INSERT INTO zawartosci(nazwa, nr_pomieszczenia, liczba, jednostka) VALUES('{name}',{id},{quantity},'{unit}')".format(
            name=new_zasob, id=new_id_pom, quantity=liczba, unit=jednostka
        )
        cursor = connections["default"].cursor()
        cursor.execute(query_delete)
        cursor.execute(query_insert)
        cursor.close()

    pomieszczenia = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    zasoby = Zasoby.objects.raw("SELECT * FROM zasoby")

    query = """SELECT * FROM zawartosci WHERE nr_pomieszczenia={a1} and nazwa='{a2}'"""

    cursor = connections["default"].cursor()
    cursor.execute(query.format(a1=id_pom, a2=zasob))
    zawartosc = cursor.fetchone()
    cursor.close()
    return render(
        request,
        "room_res_edit.html",
        {
            "Pomieszczenia": pomieszczenia,
            "Zasoby": zasoby,
            "id_pom": id_pom,
            "zasob": zasob,
            "Zawartosc": zawartosc,
        },
    )


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


def roomSys(request):
    if request.method == "POST":
        id_pom = request.POST["id_pom"]
        id_sys = request.POST["id_sys"]
        query = "DELETE FROM pomieszczenia_systemy WHERE nr_pomieszczenia = '{id_pom}' and id_systemu = {id_sys}".format(
            id_pom=id_pom, id_sys=id_sys
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT ps.id_systemu AS id, ps.nr_pomieszczenia AS id_pom, p.nazwa AS pom_name, s.nazwa AS sys_name
        FROM pomieszczenia_systemy ps INNER JOIN pomieszczenia p ON ps.nr_pomieszczenia = p.nr_pomieszczenia
        INNER JOIN systemy s ON ps.id_systemu = s.id_systemu
        WHERE UPPER(ps.nr_pomieszczenia) like '%%{a1}%%' OR UPPER(p.nazwa) like '%%{a2}%%' OR UPPER(s.nazwa) like '%%{a3}%%'"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "room_sys.html", {"out": output})

    query = """SELECT ps.id_systemu AS id, ps.nr_pomieszczenia AS id_pom, p.nazwa AS pom_name, s.nazwa AS sys_name
        FROM pomieszczenia_systemy ps INNER JOIN pomieszczenia p ON ps.nr_pomieszczenia = p.nr_pomieszczenia
        INNER JOIN systemy s ON ps.id_systemu = s.id_systemu"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "room_sys.html", {"out": output})


def roomSysNew(request):
    if request.method == "POST":
        nr_pomieszczenia = request.POST["id_pom"]
        id_systemu = request.POST["id_sys"]
        query = "INSERT INTO pomieszczenia_systemy(nr_pomieszczenia, id_systemu) VALUES({id_pom},{id_sys})".format(
            id_pom=nr_pomieszczenia, id_sys=id_systemu
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
    systemy = Systemy.objects.raw("SELECT * FROM systemy")
    pomieszczenia = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(
        request,
        "room_sys_new.html",
        {"Systemy": systemy, "Pomieszczenia": pomieszczenia},
    )


def roomSysEdit(request, id):
    id_pom = int(id.split(".")[0])
    id_sys = int(id.split(".")[1])
    if request.method == "POST":
        new_id_pom = request.POST["id_pom"]
        new_id_sys = request.POST["id_sys"]
        query = "UPDATE pomieszczenia_systemy  SET nr_pomieszczenia={new_id_pom}, id_systemu={new_id_sys} WHERE nr_pomieszczenia={id_pom} and id_systemu={id_sys}".format(
            id_pom=id_pom, id_sys=id_sys, new_id_sys=new_id_sys, new_id_pom=new_id_pom
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()
    systemy = Systemy.objects.raw("SELECT * FROM systemy")
    pomieszczenia = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    return render(
        request,
        "room_sys_edit.html",
        {
            "Systemy": systemy,
            "Pomieszczenia": pomieszczenia,
            "id_pom": id_pom,
            "id_sys": id_sys,
        },
    )


def research(request):
    if request.method == "POST":
        id = request.POST["id"]
        Badania.objects.get(id_badania=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM badania WHERE UPPER(id_badania) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(data_wykonywania) like '%%{a3}%%';"""
        output = Badania.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "research.html", {"Badania": output})

    output = Badania.objects.raw("SELECT * FROM badania")
    return render(request, "research.html", {"Badania": output})


def researchNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        date = request.POST["data"]
        Badania.objects.create(nazwa=name, opis=desc, data_wykonywania=date)
    return render(request, "research_new.html")


def researchEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        date = request.POST["data"]
        id = request.POST["id"]
        Pomieszczenia.objects.filter(nr_pomieszczenia=id).update(
            nazwa=name, opis=desc, data_wykonania=date
        )
    query = "SELECT * FROM badania WHERE id_badania={id}".format(id=id)
    output = Badania.objects.raw(query)[0]
    return render(request, "research_edit.html", {"Badanie": output})
