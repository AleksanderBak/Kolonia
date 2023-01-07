from django.shortcuts import render
from django.db import connections
from .models import (
    Pomieszczenia,
    Zasoby,
    Zawartosci,
    Systemy,
    PomieszczeniaSystemy,
    Badania,
    Pojazdy,
    Wydarzenia,
    Zadania,
    Kolonizatorzy,
    Specjalizacje,
    Doswiadczenia,
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
        query = """SELECT * FROM badania WHERE UPPER(id_badania) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(data_wykonywania) like '%%{a4}%%';"""
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
        Badania.objects.filter(id_badania=id).update(
            nazwa=name, opis=desc, data_wykonywania=date
        )
    query = "SELECT * FROM badania WHERE id_badania={id}".format(id=id)
    output = Badania.objects.raw(query)[0]
    return render(request, "research_edit.html", {"Badanie": output})


def vehicle(request):
    if request.method == "POST":
        id = request.POST["id"]
        Pojazdy.objects.get(id_pojazdu=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM pojazdy WHERE UPPER(id_pojazdu) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(przeznaczenie) like '%%{a3}%%' or UPPER(ilosc_miejsc) like '%%{a4}%%';"""
        output = Pojazdy.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "vehicle.html", {"Pojazdy": output})

    output = Pojazdy.objects.raw("SELECT * FROM pojazdy")
    return render(request, "vehicle.html", {"Pojazdy": output})


def vehicleNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        use = request.POST["przeznaczenie"]
        num = request.POST["miejsca"]
        Pojazdy.objects.create(nazwa=name, przeznaczenie=use, ilosc_miejsc=num)
    return render(request, "vehicle_new.html")


def vehicleEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        use = request.POST["przeznaczenie"]
        num = request.POST["miejsca"]
        id = request.POST["id"]
        Pojazdy.objects.filter(id_pojazdu=id).update(
            nazwa=name, przeznaczenie=use, ilosc_miejsc=num
        )
    query = "SELECT * FROM pojazdy WHERE id_pojazdu={id}".format(id=id)
    output = Pojazdy.objects.raw(query)[0]
    return render(request, "vehicle_edit.html", {"Pojazd": output})


def events(request):
    if request.method == "POST":
        id = request.POST["id"]
        Wydarzenia.objects.get(id_wydarzenia=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM wydarzenia WHERE UPPER(id_wydarzenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(potencjal_badawczy) like '%%{a4}%%' or UPPER(poziom_zagrozenia) like '%%{a5}%%' or UPPER(rodzaj_wydarzenia) like '%%{a6}%%' or UPPER(typ) like '%%{a7}%%';"""
        output = Wydarzenia.objects.raw(
            query.format(
                a1=phrase,
                a2=phrase,
                a3=phrase,
                a4=phrase,
                a5=phrase,
                a6=phrase,
                a7=phrase,
            )
        )
        return render(request, "events.html", {"Wydarzenia": output})

    output = Wydarzenia.objects.raw("SELECT * FROM wydarzenia")
    return render(request, "events.html", {"Wydarzenia": output})


def eventsNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        pot = request.POST["potencjal"]
        dang = request.POST["zagroz"]
        rodzaj = request.POST["rodzaj"]
        typ = request.POST["typ"]
        Wydarzenia.objects.create(
            nazwa=name,
            opis=desc,
            potencjal_badawczy=pot,
            poziom_zagrozenia=dang,
            rodzaj_wydarzenia=rodzaj,
            typ=typ,
        )
    return render(request, "events_new.html")


def eventsEdit(request, id):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        pot = request.POST["potencjal"]
        dang = request.POST["zagroz"]
        rodzaj = request.POST["rodzaj"]
        typ = request.POST["typ"]
        Wydarzenia.objects.filter(id_wydarzenia=id).update(
            nazwa=name,
            opis=desc,
            potencjal_badawczy=pot,
            poziom_zagrozenia=dang,
            rodzaj_wydarzenia=rodzaj,
            typ=typ,
        )
    query = "SELECT * FROM wydarzenia WHERE id_wydarzenia={id}".format(id=id)
    output = Wydarzenia.objects.raw(query)[0]
    return render(request, "events_edit.html", {"Wydarzenie": output})


def tasks(request):
    if request.method == "POST":
        id = request.POST["id"]
        Zadania.objects.get(id_zadania=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM zadania WHERE UPPER(id_zadania) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(data_wykonywania) like '%%{a4}%%';"""
        output = Zadania.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "tasks.html", {"Zadania": output})

    output = Zadania.objects.raw("SELECT * FROM zadania")
    return render(request, "tasks.html", {"Zadania": output})


def tasksNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        date = request.POST["data"]
        Zadania.objects.create(nazwa=name, opis=desc, data_wykonywania=date)
    return render(request, "tasks_new.html")


def tasksEdit(request, id):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        date = request.POST["data"]
        id = request.POST["id"]
        Zadania.objects.filter(id_zadania=id).update(
            nazwa=name, opis=desc, data_wykonywania=date
        )
    query = "SELECT * FROM zadania WHERE id_zadania={id}".format(id=id)
    output = Zadania.objects.raw(query)[0]
    return render(request, "tasks_edit.html", {"Zadanie": output})


def people(request):
    if request.method == "POST":
        id = request.POST["id"]
        Kolonizatorzy.objects.get(id_osoby=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM kolonizatorzy WHERE UPPER(id_osoby) like '%%{a1}%%' or UPPER(imie) like '%%{a2}%%' or UPPER(nazwisko) like '%%{a3}%%' or UPPER(wiek) like '%%{a4}%%' or UPPER(typ) like '%%{a5}%%';"""
        output = Kolonizatorzy.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase, a5=phrase)
        )
        return render(request, "people.html", {"Kolonizatorzy": output})

    output = Kolonizatorzy.objects.raw("SELECT * FROM kolonizatorzy")
    return render(request, "people.html", {"Kolonizatorzy": output})


def peopleNew(request):
    if request.method == "POST":
        imie = request.POST["imie"]
        nazwisko = request.POST["nazwisko"]
        wiek = request.POST["wiek"]
        typ = request.POST["typ"]
        Kolonizatorzy.objects.create(imie=imie, nazwisko=nazwisko, wiek=wiek, typ=typ)
    return render(request, "people_new.html")


def peopleEdit(request, id):
    if request.method == "POST":
        imie = request.POST["imie"]
        nazwisko = request.POST["nazwisko"]
        wiek = request.POST["wiek"]
        typ = request.POST["typ"]
        id = request.POST["id"]
        Kolonizatorzy.objects.filter(id_osoby=id).update(
            imie=imie, nazwisko=nazwisko, wiek=wiek, typ=typ
        )
    query = "SELECT * FROM kolonizatorzy WHERE id_osoby={id}".format(id=id)
    output = Kolonizatorzy.objects.raw(query)[0]
    return render(request, "people_edit.html", {"Kolonizator": output})


def specs(request):
    if request.method == "POST":
        id = request.POST["id"]
        Specjalizacje.objects.get(nazwa=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM specjalizacje WHERE UPPER(nazwa) like '%%{a1}%%' or UPPER(opis) like '%%{a2}%%';"""
        output = Specjalizacje.objects.raw(query.format(a1=phrase, a2=phrase))
        return render(request, "specs.html", {"Specjalizacje": output})

    output = Specjalizacje.objects.raw("SELECT * FROM specjalizacje")
    return render(request, "specs.html", {"Specjalizacje": output})


def specsNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        desc = request.POST["opis"]
        Specjalizacje.objects.create(nazwa=name, opis=desc)
    return render(request, "specs_new.html")


def specsEdit(request, id):
    name = ""
    if request.method == "POST":
        name = request.POST["nazwa"]
        opis = request.POST["opis"]
        Specjalizacje.objects.filter(nazwa=id).update(nazwa=name, opis=opis)

    if name != "":
        output = Specjalizacje.objects.filter(nazwa=name)[0]
    else:
        output = Specjalizacje.objects.filter(nazwa=id)[0]

    return render(request, "specs_edit.html", {"Specjalizacja": output})


def exp(request):
    if request.method == "POST":
        id = request.POST["id"]
        name = request.POST["name"]
        query = "DELETE FROM doswiadczenia WHERE nazwa = '{name}' and id_osoby = {id}".format(
            name=name, id=id
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT d.*, k.imie AS imie, k.nazwisko AS nazwisko FROM doswiadczenia d INNER JOIN kolonizatorzy k on d.id_osoby = k.id_osoby WHERE UPPER(k.imie) like '%%{a1}%%' OR UPPER(k.nazwisko) like '%%{a2}%%' OR UPPER(nazwa) like '%%{a3}%%' OR UPPER(liczba_lat) like '%%{a4}%%';"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "exp.html", {"Doswiadczenia": output})

    query = """SELECT d.*, k.imie AS imie, k.nazwisko AS nazwisko FROM doswiadczenia d INNER JOIN kolonizatorzy k on d.id_osoby = k.id_osoby;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "exp.html", {"Doswiadczenia": output})


def expNew(request):
    if request.method == "POST":
        name = request.POST["nazwa"]
        id = request.POST["id_osoby"]
        liczba_lat = request.POST["liczba_lat"]
        query = "INSERT INTO doswiadczenia(nazwa, id_osoby, liczba_lat) VALUES('{name}',{id},{years})".format(
            name=name, id=id, years=liczba_lat
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw("SELECT * FROM kolonizatorzy")
    specjalizacje = Specjalizacje.objects.raw("SELECT * FROM specjalizacje")
    return render(
        request,
        "exp_new.html",
        {"Kolonizatorzy": kolonizatorzy, "Specjalizacje": specjalizacje},
    )


def expEdit(request, id):
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
