from django.shortcuts import render
from django.db import connections, transaction
from datetime import datetime
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
    KolonizatorzyZadania,
    KolonizatorzyBadania,
    BadaniaPomieszczenia,
    ZadaniaPomieszczenia,
)


def dashboard(request):
    if request.method == "GET":
        if "level" in request.GET:
            level = request.GET["level"]
            if level == "":
                level = 0
            else:
                level = int(level)
            if level > 10:
                level = 10
            elif level < 0:
                level = 0
        else:
            level = 5
    else:
        level = 5

    if request.method == "POST":
        pomieszczenie = request.POST["pomieszczenie"]
        liczba = request.POST["liczba"]
        jednostka = request.POST["jednostka"]
        zasob = request.POST["zasob"]
        cursor = connections["default"].cursor()
        cursor.callproc("DODAJZASOB", [zasob, liczba, pomieszczenie, jednostka])
        cursor.close()

    pojazdy = Pojazdy.objects.count()
    badania = Badania.objects.filter(data_wykonywania__gt=datetime.today()).count()
    zadania = Zadania.objects.filter(data_wykonywania__gt=datetime.today()).count()
    kolonizatorzy = Kolonizatorzy.objects.count()
    pomieszczenia = Pomieszczenia.objects.count()
    pomieszczeniaAll = Pomieszczenia.objects.raw("SELECT * FROM pomieszczenia")
    cursor = connections["default"].cursor()
    niebezp = cursor.callfunc("PoliczNiebezpieczne", int, [level])
    cursor.execute("SELECT count(id_osoby) FROM kolonizatorzy WHERE typ = 'Badawczy';")
    kolonizatorzy_badawczy = cursor.fetchone()
    cursor.execute(
        "SELECT * FROM wydarzenia ORDER BY poziom_zagrozenia desc, potencjal_badawczy desc;"
    )
    najwazniejsze_wydarzenia = cursor.fetchall()
    cursor.close()
    cursor = connections["default"].cursor()
    return render(
        request,
        "dashboard.html",
        {
            "PojazdyCount": pojazdy,
            "BadaniaCount": badania,
            "ZadaniaCount": zadania,
            "Niebezp": niebezp,
            "KolonizatorzyCount": kolonizatorzy,
            "PomieszczeniaCount": pomieszczenia,
            "Pomieszczenia": pomieszczeniaAll,
            "Badawczy": kolonizatorzy_badawczy,
            "Wydarzenia": najwazniejsze_wydarzenia,
            "Poziom": level,
        },
    )


def rooms(request):
    if request.method == "POST":
        id = request.POST["id"]
        Pomieszczenia.objects.get(nr_pomieszczenia=id).delete()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT * FROM pomieszczenia WHERE UPPER(nr_pomieszczenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' ORDER BY nr_pomieszczenia;"""
        output = Pomieszczenia.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase)
        )
        return render(request, "rooms.html", {"Pomieszczenia": output})

    output = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )
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

    output = Zasoby.objects.raw("SELECT * FROM zasoby ORDER BY nazwa")
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
    zasoby = Zasoby.objects.raw("SELECT * FROM zasoby ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )
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
        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )
    zasoby = Zasoby.objects.raw("SELECT * FROM zasoby ORDER BY nazwa")

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
        query = """SELECT * FROM systemy WHERE id_systemu like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' ORDER BY nazwa;"""
        output = Systemy.objects.raw(query.format(a1=phrase, a2=phrase, a3=phrase))
        return render(request, "systems.html", {"Systemy": output})

    output = Systemy.objects.raw("SELECT * FROM systemy ORDER BY nazwa")
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
    systemy = Systemy.objects.raw("SELECT * FROM systemy ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )
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
    systemy = Systemy.objects.raw("SELECT * FROM systemy ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )
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
        query = """SELECT * FROM badania WHERE UPPER(id_badania) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(data_wykonywania) like '%%{a4}%%' ORDER BY nazwa;"""
        output = Badania.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "research.html", {"Badania": output})

    output = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
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
        query = """SELECT * FROM pojazdy WHERE UPPER(id_pojazdu) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(przeznaczenie) like '%%{a3}%%' or UPPER(ilosc_miejsc) like '%%{a4}%%' ORDER BY nazwa;"""
        output = Pojazdy.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "vehicle.html", {"Pojazdy": output})

    output = Pojazdy.objects.raw("SELECT * FROM pojazdy ORDER BY nazwa")
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
        query = """SELECT * FROM wydarzenia WHERE UPPER(id_wydarzenia) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(potencjal_badawczy) like '%%{a4}%%' or UPPER(poziom_zagrozenia) like '%%{a5}%%' or UPPER(rodzaj_wydarzenia) like '%%{a6}%%' or UPPER(typ) like '%%{a7}%%' ORDER BY nazwa;"""
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

    output = Wydarzenia.objects.raw("SELECT * FROM wydarzenia ORDER BY nazwa")
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
        query = """SELECT * FROM zadania WHERE UPPER(id_zadania) like '%%{a1}%%' or UPPER(nazwa) like '%%{a2}%%' or UPPER(opis) like '%%{a3}%%' or UPPER(data_wykonywania) like '%%{a4}%%' ORDER BY nazwa;"""
        output = Zadania.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase)
        )
        return render(request, "tasks.html", {"Zadania": output})

    output = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
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
        query = """SELECT * FROM kolonizatorzy WHERE UPPER(id_osoby) like '%%{a1}%%' or UPPER(imie) like '%%{a2}%%' or UPPER(nazwisko) like '%%{a3}%%' or UPPER(wiek) like '%%{a4}%%' or UPPER(typ) like '%%{a5}%%' ORDER BY imie,nazwisko;"""
        output = Kolonizatorzy.objects.raw(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase, a5=phrase)
        )
        return render(request, "people.html", {"Kolonizatorzy": output})

    output = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy ORDER BY imie,nazwisko"
    )
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

        if typ == "Zwykły":
            block = KolonizatorzyBadania.objects.filter(id_osoby=id).count()
        elif typ == "Badawczy":
            block = KolonizatorzyZadania.objects.filter(id_osoby=id).count()

        if block > 0:
            raise KeyError

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
        query = """SELECT * FROM specjalizacje WHERE UPPER(nazwa) like '%%{a1}%%' or UPPER(opis) like '%%{a2}%%' ORDER BY nazwa;"""
        output = Specjalizacje.objects.raw(query.format(a1=phrase, a2=phrase))
        return render(request, "specs.html", {"Specjalizacje": output})

    output = Specjalizacje.objects.raw("SELECT * FROM specjalizacje ORDER BY nazwa")
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

    query = """SELECT d.*, k.imie AS imie, k.nazwisko AS nazwisko FROM doswiadczenia d INNER JOIN kolonizatorzy k on d.id_osoby = k.id_osoby ORDER BY k.imie,k.nazwisko;"""
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

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy ORDER BY imie,nazwisko"
    )
    specjalizacje = Specjalizacje.objects.raw(
        "SELECT * FROM specjalizacje ORDER BY nazwa"
    )
    return render(
        request,
        "exp_new.html",
        {"Kolonizatorzy": kolonizatorzy, "Specjalizacje": specjalizacje},
    )


def expEdit(request, id):
    id_os = int(id.split(".")[0])
    nazwa = id.split(".")[1]

    if request.method == "POST":
        new_id_os = request.POST["id_os"]
        new_nazwa = request.POST["nazwa"]
        lata = request.POST["lata"]

        query_delete = "DELETE FROM doswiadczenia WHERE id_osoby = {osoba} and nazwa = '{nazwa}'".format(
            osoba=id_os, nazwa=nazwa
        )

        query_insert = "INSERT INTO doswiadczenia(id_osoby, nazwa, liczba_lat) VALUES({id_os},'{nazwa}',{lata})".format(
            id_os=new_id_os, nazwa=new_nazwa, lata=lata
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy ORDER BY imie,nazwisko"
    )
    specjalizacje = Specjalizacje.objects.raw(
        "SELECT * FROM specjalizacje ORDER BY nazwa"
    )

    query = """SELECT * FROM doswiadczenia WHERE id_osoby={a1} and nazwa='{a2}'"""

    cursor = connections["default"].cursor()
    cursor.execute(query.format(a1=id_os, a2=nazwa))
    doswiadczenie = cursor.fetchone()
    cursor.close()
    return render(
        request,
        "exp_edit.html",
        {
            "Kolonizatorzy": kolonizatorzy,
            "Specjalizacje": specjalizacje,
            "Doswiadczenie": doswiadczenie,
            "id_os": id_os,
            "nazwa": nazwa,
        },
    )


def peopleTasks(request):
    if request.method == "POST":
        id_os = request.POST["id_os"]
        id_zad = request.POST["id_zad"]
        query = "DELETE FROM kolonizatorzy_zadania WHERE id_osoby = '{id_os}' and id_zadania = {id_zad}".format(
            id_os=id_os, id_zad=id_zad
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT kz.*, k.imie AS imie, k.nazwisko AS nazwisko, z.nazwa AS zadanie FROM kolonizatorzy_zadania kz INNER JOIN kolonizatorzy k on kz.id_osoby = k.id_osoby INNER JOIN zadania z on kz.id_zadania = z.id_zadania WHERE UPPER(k.imie) like '%%{a1}%%' OR UPPER(k.nazwisko) like '%%{a2}%%' OR UPPER(z.nazwa) like '%%{a3}%%' OR UPPER(kz.id_osoby) like '%%{a4}%%' OR UPPER(kz.id_zadania) like '%%{a5}%%' ORDER BY k.imie,k.nazwisko;"""
        cursor = connections["default"].cursor()
        cursor.execute(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase, a5=phrase)
        )
        output = cursor.fetchall()
        cursor.close()
        return render(request, "people_tasks.html", {"KolonizatorzyZadania": output})

    query = """SELECT kz.*, k.imie AS imie, k.nazwisko AS nazwisko, z.nazwa AS zadanie FROM kolonizatorzy_zadania kz INNER JOIN kolonizatorzy k on kz.id_osoby = k.id_osoby INNER JOIN zadania z on kz.id_zadania = z.id_zadania ORDER BY k.imie, k.nazwisko;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "people_tasks.html", {"KolonizatorzyZadania": output})


def peopleTasksNew(request):
    if request.method == "POST":
        id_os = request.POST["id_osoby"]
        id_zad = request.POST["id_zadania"]
        query = "INSERT INTO kolonizatorzy_zadania(id_osoby, id_zadania) VALUES('{id_os}',{id_zad})".format(
            id_os=id_os, id_zad=id_zad
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy WHERE typ = 'Zwykły' ORDER BY imie,nazwisko"
    )
    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")

    return render(
        request,
        "people_tasks_new.html",
        {"Kolonizatorzy": kolonizatorzy, "Zadania": zadania},
    )


def peopleTasksEdit(request, id):
    id_os = int(id.split(".")[0])
    id_zadania = int(id.split(".")[1])

    if request.method == "POST":
        new_id_os = request.POST["id_osoby"]
        new_id_zad = request.POST["id_zadania"]

        query_delete = "DELETE FROM kolonizatorzy_zadania WHERE id_osoby = {osoba} and id_zadania = {zadanie}".format(
            osoba=id_os, zadanie=id_zadania
        )

        query_insert = "INSERT INTO kolonizatorzy_zadania(id_osoby, id_zadania) VALUES({id_os},{id_zad})".format(
            id_os=new_id_os, id_zad=new_id_zad
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy WHERE typ = 'Zwykły' ORDER BY imie,nazwisko"
    )
    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")

    return render(
        request,
        "people_tasks_edit.html",
        {
            "Kolonizatorzy": kolonizatorzy,
            "Zadania": zadania,
            "id_kolonizatora": id_os,
            "id_zadania": id_zadania,
        },
    )


def peopleResearch(request):
    if request.method == "POST":
        id_os = request.POST["id_os"]
        id_bad = request.POST["id_bad"]
        query = "DELETE FROM kolonizatorzy_badania WHERE id_osoby = '{id_os}' and id_badania = {id_bad}".format(
            id_os=id_os, id_bad=id_bad
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT kb.*, k.imie AS imie, k.nazwisko AS nazwisko, b.nazwa AS zadanie FROM kolonizatorzy_badania kb INNER JOIN kolonizatorzy k on kb.id_osoby = k.id_osoby INNER JOIN badania b on kb.id_badania = b.id_badania WHERE UPPER(k.imie) like '%%{a1}%%' OR UPPER(k.nazwisko) like '%%{a2}%%' OR UPPER(b.nazwa) like '%%{a3}%%' OR UPPER(kb.id_osoby) like '%%{a4}%%' OR UPPER(kb.id_badania) like '%%{a5}%%' ORDER BY k.imie,k.nazwisko;"""
        cursor = connections["default"].cursor()
        cursor.execute(
            query.format(a1=phrase, a2=phrase, a3=phrase, a4=phrase, a5=phrase)
        )
        output = cursor.fetchall()
        cursor.close()
        return render(request, "people_tasks.html", {"KolonizatorzyZadania": output})

    query = """SELECT kb.*, k.imie AS imie, k.nazwisko AS nazwisko, b.nazwa AS zadanie FROM kolonizatorzy_badania kb INNER JOIN kolonizatorzy k on kb.id_osoby = k.id_osoby INNER JOIN badania b on kb.id_badania = b.id_badania ORDER BY k.imie,k.nazwisko;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "people_research.html", {"KolonizatorzyBadania": output})


def peopleResearchNew(request):
    if request.method == "POST":
        id_os = request.POST["id_osoby"]
        id_bad = request.POST["id_badania"]
        query = "INSERT INTO kolonizatorzy_badania(id_osoby, id_badania) VALUES('{id_os}',{id_bad})".format(
            id_os=id_os, id_bad=id_bad
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy WHERE typ = 'Badawczy' ORDER BY imie,nazwisko"
    )
    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")

    return render(
        request,
        "people_research_new.html",
        {"Kolonizatorzy": kolonizatorzy, "Badania": badania},
    )


def peopleResearchEdit(request, id):
    id_os = int(id.split(".")[0])
    id_badania = int(id.split(".")[1])

    if request.method == "POST":
        new_id_os = request.POST["id_osoby"]
        new_id_bad = request.POST["id_badania"]

        query_delete = "DELETE FROM kolonizatorzy_badania WHERE id_osoby = {osoba} and id_badania = {badanie}".format(
            osoba=id_os, badanie=id_badania
        )

        query_insert = "INSERT INTO kolonizatorzy_badania(id_osoby, id_badania) VALUES({id_os},{id_bad})".format(
            id_os=new_id_os, id_bad=new_id_bad
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    kolonizatorzy = Kolonizatorzy.objects.raw(
        "SELECT * FROM kolonizatorzy WHERE typ = 'Badawczy' ORDER BY imie,nazwisko"
    )
    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")

    return render(
        request,
        "people_research_edit.html",
        {
            "Kolonizatorzy": kolonizatorzy,
            "Badania": badania,
            "id_kolonizatora": id_os,
            "id_badania": id_badania,
        },
    )


def tasksRooms(request):
    if request.method == "POST":
        id_pom = request.POST["id_pom"]
        id_zad = request.POST["id_zad"]
        query = "DELETE FROM zadania_pomieszczenia WHERE id_zadania = '{id_zad}' and nr_pomieszczenia = {id_pom}".format(
            id_zad=id_zad, id_pom=id_pom
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT zp.*, z.nazwa AS zadanie, p.nazwa AS pomieszczenie FROM zadania_pomieszczenia zp INNER JOIN zadania z on zp.id_zadania = z.id_zadania INNER JOIN pomieszczenia p on zp.nr_pomieszczenia = p.nr_pomieszczenia WHERE UPPER(p.nazwa) like '%%{a1}%%' OR UPPER(z.nazwa) like '%%{a2}%%' OR UPPER(zp.nr_pomieszczenia) like '%%{a3}%%' ORDER BY z.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "tasks_rooms.html", {"ZadaniaPomieszczenia": output})

    query = """SELECT zp.*, z.nazwa AS zadanie, p.nazwa AS pomieszczenie FROM zadania_pomieszczenia zp INNER JOIN zadania z on zp.id_zadania = z.id_zadania INNER JOIN pomieszczenia p on zp.nr_pomieszczenia = p.nr_pomieszczenia ORDER BY z.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "tasks_rooms.html", {"ZadaniaPomieszczenia": output})


def tasksRoomsNew(request):
    if request.method == "POST":
        id_zad = request.POST["id_zad"]
        id_pom = request.POST["id_pom"]
        query = "INSERT INTO zadania_pomieszczenia(id_zadania, nr_pomieszczenia) VALUES({id_zad},{id_pom})".format(
            id_zad=id_zad, id_pom=id_pom
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )

    return render(
        request,
        "tasks_rooms_new.html",
        {"Zadania": zadania, "Pomieszczenia": pomieszczenia},
    )


def tasksRoomsEdit(request, id):
    id_zad = int(id.split(".")[0])
    id_pom = int(id.split(".")[1])

    if request.method == "POST":
        new_id_zad = request.POST["id_zad"]
        new_id_pom = request.POST["id_pom"]

        query_delete = "DELETE FROM zadania_pomieszczenia WHERE id_zadania = {id_zad} and nr_pomieszczenia = {id_pom}".format(
            id_zad=id_zad, id_pom=id_pom
        )

        query_insert = "INSERT INTO zadania_pomieszczenia(id_zadania, nr_pomieszczenia) VALUES({id_zad},{id_pom})".format(
            id_zad=new_id_zad, id_pom=new_id_pom
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )

    return render(
        request,
        "tasks_rooms_edit.html",
        {
            "Zadania": zadania,
            "Pomieszczenia": pomieszczenia,
            "id_zadania": id_zad,
            "id_pomieszczenia": id_pom,
        },
    )


def researchesRooms(request):
    if request.method == "POST":
        id_pom = request.POST["id_pom"]
        id_bad = request.POST["id_bad"]
        query = "DELETE FROM badania_pomieszczenia WHERE id_badania = {id_bad} and nr_pomieszczenia = {id_pom}".format(
            id_bad=id_bad, id_pom=id_pom
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT bp.*, b.nazwa AS badanie, p.nazwa AS pomieszczenie FROM badania_pomieszczenia bp INNER JOIN badania b on bp.id_badania = b.id_badania INNER JOIN pomieszczenia p on bp.nr_pomieszczenia = p.nr_pomieszczenia WHERE UPPER(p.nazwa) like '%%{a1}%%' OR UPPER(b.nazwa) like '%%{a2}%%' OR UPPER(bp.nr_pomieszczenia) like '%%{a3}%%' ORDER BY b.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(
            request, "researches_rooms.html", {"BadaniaPomieszczenia": output}
        )

    query = """SELECT bp.*, b.nazwa AS badanie, p.nazwa AS pomieszczenie FROM badania_pomieszczenia bp INNER JOIN badania b on bp.id_badania = b.id_badania INNER JOIN pomieszczenia p on bp.nr_pomieszczenia = p.nr_pomieszczenia ORDER BY b.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "researches_rooms.html", {"BadaniaPomieszczenia": output})


def researchesRoomsNew(request):
    if request.method == "POST":
        id_bad = request.POST["id_bad"]
        id_pom = request.POST["id_pom"]
        query = "INSERT INTO badania_pomieszczenia(id_badania, nr_pomieszczenia) VALUES({id_bad},{id_pom})".format(
            id_bad=id_bad, id_pom=id_pom
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )

    return render(
        request,
        "researches_rooms_new.html",
        {"Badania": badania, "Pomieszczenia": pomieszczenia},
    )


def researchesRoomsEdit(request, id):
    id_bad = int(id.split(".")[0])
    id_pom = int(id.split(".")[1])

    if request.method == "POST":
        new_id_bad = request.POST["id_bad"]
        new_id_pom = request.POST["id_pom"]

        query_delete = "DELETE FROM badania_pomieszczenia WHERE id_badania = {id_bad} and nr_pomieszczenia = {id_pom}".format(
            id_bad=id_bad, id_pom=id_pom
        )

        query_insert = "INSERT INTO badania_pomieszczenia(id_badania, nr_pomieszczenia) VALUES({id_bad},{id_pom})".format(
            id_bad=new_id_bad, id_pom=new_id_pom
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    pomieszczenia = Pomieszczenia.objects.raw(
        "SELECT * FROM pomieszczenia ORDER BY nr_pomieszczenia"
    )

    return render(
        request,
        "researches_rooms_edit.html",
        {
            "Badania": badania,
            "Pomieszczenia": pomieszczenia,
            "id_badania": id_bad,
            "id_pomieszczenia": id_pom,
        },
    )


def tasksVehicles(request):
    if request.method == "POST":
        id_zad = request.POST["id_zad"]
        id_poj = request.POST["id_poj"]
        query = "DELETE FROM zadania_pojazdy WHERE id_zadania = {id_zad} and id_pojazdu = {id_poj}".format(
            id_zad=id_zad, id_poj=id_poj
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT zp.*, z.nazwa AS zadanie, p.nazwa AS pojazd FROM zadania_pojazdy zp INNER JOIN zadania z on zp.id_zadania = z.id_zadania INNER JOIN pojazdy p on zp.id_pojazdu = p.id_pojazdu WHERE UPPER(p.nazwa) like '%%{a1}%%' OR UPPER(z.nazwa) like '%%{a2}%%' OR UPPER(p.id_pojazdu) like '%%{a3}%%' ORDER BY z.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "tasks_vehicles.html", {"ZadaniaPojazdy": output})

    query = """SELECT zp.*, z.nazwa AS zadanie, p.nazwa AS pojazd FROM zadania_pojazdy zp INNER JOIN zadania z on zp.id_zadania = z.id_zadania INNER JOIN pojazdy p on zp.id_pojazdu = p.id_pojazdu ORDER BY z.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "tasks_vehicles.html", {"ZadaniaPojazdy": output})


def tasksVehiclesNew(request):
    if request.method == "POST":
        id_zad = request.POST["id_zad"]
        id_poj = request.POST["id_poj"]
        query = "INSERT INTO zadania_pojazdy(id_zadania, id_pojazdu) VALUES({id_zad},{id_poj})".format(
            id_zad=id_zad, id_poj=id_poj
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    pojazdy = Pojazdy.objects.raw("SELECT * FROM pojazdy ORDER BY nazwa")

    return render(
        request,
        "tasks_vehicles_new.html",
        {"Zadania": zadania, "Pojazdy": pojazdy},
    )


def tasksVehiclesEdit(request, id):
    id_zad = int(id.split(".")[0])
    id_poj = int(id.split(".")[1])

    if request.method == "POST":
        new_id_zad = request.POST["id_zad"]
        new_id_poj = request.POST["id_poj"]

        query_delete = "DELETE FROM zadania_pojazdy WHERE id_zadania = {id_zad} and id_pojazdu = {id_poj}".format(
            id_zad=id_zad, id_poj=id_poj
        )

        query_insert = "INSERT INTO zadania_pojazdy(id_zadania, id_pojazdu) VALUES({id_zad},{id_poj})".format(
            id_zad=new_id_zad, id_poj=new_id_poj
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    pojazdy = Pojazdy.objects.raw("SELECT * FROM pojazdy ORDER BY nazwa")

    return render(
        request,
        "tasks_vehicles_edit.html",
        {
            "Zadania": zadania,
            "Pojazdy": pojazdy,
            "id_zadania": id_zad,
            "id_pojazdu": id_poj,
        },
    )


def researchesVehicles(request):
    if request.method == "POST":
        id_bad = request.POST["id_bad"]
        id_poj = request.POST["id_poj"]
        query = "DELETE FROM badania_pojazdy WHERE id_badania = {id_bad} and id_pojazdu = {id_poj}".format(
            id_bad=id_bad, id_poj=id_poj
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT bp.*, b.nazwa AS badanie, p.nazwa AS pojazd FROM badania_pojazdy bp INNER JOIN badania b on bp.id_badania = b.id_badania INNER JOIN pojazdy p on bp.id_pojazdu = p.id_pojazdu WHERE UPPER(p.nazwa) like '%%{a1}%%' OR UPPER(b.nazwa) like '%%{a2}%%' OR UPPER(p.id_pojazdu) like '%%{a3}%%' ORDER BY b.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase, a3=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "researches_vehicles.html", {"BadaniaPojazdy": output})

    query = """SELECT bp.*, b.nazwa AS badanie, p.nazwa AS pojazd FROM badania_pojazdy bp INNER JOIN badania b on bp.id_badania = b.id_badania INNER JOIN pojazdy p on bp.id_pojazdu = p.id_pojazdu ORDER BY b.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "researches_vehicles.html", {"BadaniaPojazdy": output})


def researchesVehiclesNew(request):
    if request.method == "POST":
        id_bad = request.POST["id_bad"]
        id_poj = request.POST["id_poj"]
        query = "INSERT INTO badania_pojazdy(id_badania, id_pojazdu) VALUES({id_bad},{id_poj})".format(
            id_bad=id_bad, id_poj=id_poj
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    pojazdy = Pojazdy.objects.raw("SELECT * FROM pojazdy ORDER BY nazwa")

    return render(
        request,
        "researches_vehicles_new.html",
        {"Badania": badania, "Pojazdy": pojazdy},
    )


def researchesVehiclesEdit(request, id):
    id_bad = int(id.split(".")[0])
    id_poj = int(id.split(".")[1])

    if request.method == "POST":
        new_id_bad = request.POST["id_bad"]
        new_id_poj = request.POST["id_poj"]

        query_delete = "DELETE FROM badania_pojazdy WHERE id_badania = {id_bad} and id_pojazdu = {id_poj}".format(
            id_bad=id_bad, id_poj=id_poj
        )

        query_insert = "INSERT INTO badania_pojazdy(id_badania, id_pojazdu) VALUES({id_bad},{id_poj})".format(
            id_bad=new_id_bad, id_poj=new_id_poj
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    pojazdy = Pojazdy.objects.raw("SELECT * FROM pojazdy ORDER BY nazwa")

    return render(
        request,
        "researches_vehicles_edit.html",
        {
            "Badania": badania,
            "Pojazdy": pojazdy,
            "id_badania": id_bad,
            "id_pojazdu": id_poj,
        },
    )


def researchesEvents(request):
    if request.method == "POST":
        id_bad = request.POST["id_bad"]
        id_wyd = request.POST["id_wyd"]
        query = "DELETE FROM badania_wydarzenia WHERE id_badania = {id_bad} and id_wydarzenia = {id_wyd}".format(
            id_bad=id_bad, id_wyd=id_wyd
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT bw.*, b.nazwa AS badanie, w.nazwa AS wydarzenie FROM badania_wydarzenia bw INNER JOIN badania b on bw.id_badania = b.id_badania INNER JOIN wydarzenia w on bw.id_wydarzenia = w.id_wydarzenia WHERE UPPER(w.nazwa) like '%%{a1}%%' OR UPPER(b.nazwa) like '%%{a2}%%' ORDER BY b.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "researches_events.html", {"BadaniaWydarzenia": output})

    query = """SELECT bw.*, b.nazwa AS badanie, w.nazwa AS wydarzenie FROM badania_wydarzenia bw INNER JOIN badania b on bw.id_badania = b.id_badania INNER JOIN wydarzenia w on bw.id_wydarzenia = w.id_wydarzenia ORDER BY b.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "researches_events.html", {"BadaniaWydarzenia": output})


def researchesEventsNew(request):
    if request.method == "POST":
        id_bad = request.POST["id_bad"]
        id_wyd = request.POST["id_wyd"]
        query = "INSERT INTO badania_wydarzenia(id_badania, id_wydarzenia) VALUES({id_bad},{id_wyd})".format(
            id_bad=id_bad, id_wyd=id_wyd
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    wydarzenia = Wydarzenia.objects.raw("SELECT * FROM wydarzenia ORDER BY nazwa")

    return render(
        request,
        "researches_events_new.html",
        {"Badania": badania, "Wydarzenia": wydarzenia},
    )


def researchesEventsEdit(request, id):
    id_bad = int(id.split(".")[0])
    id_wyd = int(id.split(".")[1])

    if request.method == "POST":
        new_id_bad = request.POST["id_bad"]
        new_id_wyd = request.POST["id_wyd"]

        query_delete = "DELETE FROM badania_wydarzenia WHERE id_badania = {id_bad} and id_wydarzenia = {id_wyd}".format(
            id_bad=id_bad, id_wyd=id_wyd
        )

        query_insert = "INSERT INTO badania_wydarzenia(id_badania, id_wydarzenia) VALUES({id_bad},{id_wyd})".format(
            id_bad=new_id_bad, id_wyd=new_id_wyd
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    badania = Badania.objects.raw("SELECT * FROM badania ORDER BY nazwa")
    wydarzenia = Wydarzenia.objects.raw("SELECT * FROM wydarzenia ORDER BY nazwa")

    return render(
        request,
        "researches_events_edit.html",
        {
            "Badania": badania,
            "Wydarzenia": wydarzenia,
            "id_badania": id_bad,
            "id_wydarzenia": id_wyd,
        },
    )


def tasksEvents(request):
    if request.method == "POST":
        id_zad = request.POST["id_zad"]
        id_wyd = request.POST["id_wyd"]
        query = "DELETE FROM wydarzenia_zadania WHERE id_zadania = {id_zad} and id_wydarzenia = {id_wyd}".format(
            id_zad=id_zad, id_wyd=id_wyd
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    if request.method == "GET" and "search" in request.GET:
        phrase = request.GET["search"].upper()
        query = """SELECT zw.*, z.nazwa AS zadanie, w.nazwa AS wydarzenie FROM wydarzenia_zadania zw INNER JOIN zadania z on zw.id_zadania = z.id_zadania INNER JOIN wydarzenia w on zw.id_wydarzenia = w.id_wydarzenia WHERE UPPER(w.nazwa) like '%%{a1}%%' OR UPPER(z.nazwa) like '%%{a2}%%' ORDER BY z.nazwa;"""
        cursor = connections["default"].cursor()
        cursor.execute(query.format(a1=phrase, a2=phrase))
        output = cursor.fetchall()
        cursor.close()
        return render(request, "tasks_events.html", {"ZadaniaWydarzenia": output})

    query = """SELECT zw.*, z.nazwa AS zadanie, w.nazwa AS wydarzenie FROM wydarzenia_zadania zw INNER JOIN zadania z on zw.id_zadania = z.id_zadania INNER JOIN wydarzenia w on zw.id_wydarzenia = w.id_wydarzenia ORDER BY z.nazwa;"""
    cursor = connections["default"].cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    cursor.close()
    return render(request, "tasks_events.html", {"ZadaniaWydarzenia": output})


def tasksEventsNew(request):
    if request.method == "POST":
        id_zad = request.POST["id_zad"]
        id_wyd = request.POST["id_wyd"]
        query = "INSERT INTO wydarzenia_zadania(id_zadania, id_wydarzenia) VALUES({id_zad},{id_wyd})".format(
            id_zad=id_zad, id_wyd=id_wyd
        )
        cursor = connections["default"].cursor()
        cursor.execute(query)
        cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    wydarzenia = Wydarzenia.objects.raw("SELECT * FROM wydarzenia ORDER BY nazwa")

    return render(
        request,
        "tasks_events_new.html",
        {"Zadania": zadania, "Wydarzenia": wydarzenia},
    )


def tasksEventsEdit(request, id):
    id_zad = int(id.split(".")[0])
    id_wyd = int(id.split(".")[1])

    if request.method == "POST":
        new_id_zad = request.POST["id_zad"]
        new_id_wyd = request.POST["id_wyd"]

        query_delete = "DELETE FROM wydarzenia_zadania WHERE id_zadania = {id_zad} and id_wydarzenia = {id_wyd}".format(
            id_zad=id_zad, id_wyd=id_wyd
        )

        query_insert = "INSERT INTO wydarzenia_zadania(id_zadania, id_wydarzenia) VALUES({id_zad},{id_wyd})".format(
            id_zad=new_id_zad, id_wyd=new_id_wyd
        )
        cursor = connections["default"].cursor()

        try:
            transaction.set_autocommit(False)
            cursor.execute(query_delete)
            cursor.execute(query_insert)
        except:
            transaction.rollback()
            raise NameError
        finally:
            transaction.set_autocommit(True)
            cursor.close()

    zadania = Zadania.objects.raw("SELECT * FROM zadania ORDER BY nazwa")
    wydarzenia = Wydarzenia.objects.raw("SELECT * FROM wydarzenia ORDER BY nazwa")

    return render(
        request,
        "tasks_events_edit.html",
        {
            "Zadania": zadania,
            "Wydarzenia": wydarzenia,
            "id_zadania": id_zad,
            "id_wydarzenia": id_wyd,
        },
    )
