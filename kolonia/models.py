from django.db import models

# Create your models here.
class Pomieszczenia(models.Model):
    nr_pomieszczenia = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pomieszczenia"


class Zasoby(models.Model):
    nazwa = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = "zasoby"


class Zawartosci(models.Model):
    liczba = models.DecimalField(max_digits=6, decimal_places=2)
    nr_pomieszczenia = models.OneToOneField(
        Pomieszczenia, models.DO_NOTHING, db_column="nr_pomieszczenia", primary_key=True
    )
    jednostka = models.CharField(max_length=32)
    nazwa = models.ForeignKey(Zasoby, models.DO_NOTHING, db_column="nazwa")

    class Meta:
        managed = False
        db_table = "zawartosci"
        unique_together = (("nr_pomieszczenia", "nazwa"),)


class Systemy(models.Model):
    id_systemu = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "systemy"


class PomieszczeniaSystemy(models.Model):
    nr_pomieszczenia = models.OneToOneField(
        Pomieszczenia, models.DO_NOTHING, db_column="nr_pomieszczenia", primary_key=True
    )
    id_systemu = models.ForeignKey("Systemy", models.DO_NOTHING, db_column="id_systemu")

    class Meta:
        managed = False
        db_table = "pomieszczenia_systemy"
        unique_together = (("nr_pomieszczenia", "id_systemu"),)


class Badania(models.Model):
    id_badania = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256)
    data_wykonywania = models.DateField()

    class Meta:
        managed = False
        db_table = "badania"


class Pojazdy(models.Model):
    id_pojazdu = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    przeznaczenie = models.CharField(max_length=32)
    ilosc_miejsc = models.IntegerField()

    class Meta:
        managed = False
        db_table = "pojazdy"


class Wydarzenia(models.Model):
    id_wydarzenia = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256)
    potencjal_badawczy = models.IntegerField()
    poziom_zagrozenia = models.IntegerField()
    rodzaj_wydarzenia = models.CharField(max_length=32)
    typ = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "wydarzenia"


class Zadania(models.Model):
    id_zadania = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256)
    data_wykonywania = models.DateField()

    class Meta:
        managed = False
        db_table = "zadania"


class Kolonizatorzy(models.Model):
    id_osoby = models.IntegerField(primary_key=True)
    imie = models.CharField(max_length=32)
    nazwisko = models.CharField(max_length=32)
    wiek = models.IntegerField()
    typ = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "kolonizatorzy"


class Specjalizacje(models.Model):
    nazwa = models.CharField(primary_key=True, max_length=32)
    opis = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "specjalizacje"


class Doswiadczenia(models.Model):
    id_osoby = models.OneToOneField(
        "Kolonizatorzy", models.DO_NOTHING, db_column="id_osoby", primary_key=True
    )
    nazwa = models.ForeignKey("Specjalizacje", models.DO_NOTHING, db_column="nazwa")
    liczba_lat = models.IntegerField()

    class Meta:
        managed = False
        db_table = "doswiadczenia"
        unique_together = (("id_osoby", "nazwa"),)


class KolonizatorzyBadania(models.Model):
    id_osoby = models.OneToOneField(
        Kolonizatorzy, models.DO_NOTHING, db_column="id_osoby", primary_key=True
    )
    id_badania = models.ForeignKey(Badania, models.DO_NOTHING, db_column="id_badania")

    class Meta:
        managed = False
        db_table = "kolonizatorzy_badania"
        unique_together = (("id_osoby", "id_badania"),)


class KolonizatorzyZadania(models.Model):
    id_osoby = models.OneToOneField(
        Kolonizatorzy, models.DO_NOTHING, db_column="id_osoby", primary_key=True
    )
    id_zadania = models.ForeignKey("Zadania", models.DO_NOTHING, db_column="id_zadania")

    class Meta:
        managed = False
        db_table = "kolonizatorzy_zadania"
        unique_together = (("id_osoby", "id_zadania"),)


class ZadaniaPomieszczenia(models.Model):
    id_zadania = models.OneToOneField(
        Zadania, models.DO_NOTHING, db_column="id_zadania", primary_key=True
    )
    nr_pomieszczenia = models.ForeignKey(
        Pomieszczenia, models.DO_NOTHING, db_column="nr_pomieszczenia"
    )

    class Meta:
        managed = False
        db_table = "zadania_pomieszczenia"
        unique_together = (("id_zadania", "nr_pomieszczenia"),)


class BadaniaPomieszczenia(models.Model):
    id_badania = models.OneToOneField(
        Badania, models.DO_NOTHING, db_column="id_badania", primary_key=True
    )
    nr_pomieszczenia = models.ForeignKey(
        "Pomieszczenia", models.DO_NOTHING, db_column="nr_pomieszczenia"
    )

    class Meta:
        managed = False
        db_table = "badania_pomieszczenia"
        unique_together = (("id_badania", "nr_pomieszczenia"),)


class ZadaniaPojazdy(models.Model):
    id_zadania = models.OneToOneField(
        Zadania, models.DO_NOTHING, db_column="id_zadania", primary_key=True
    )
    id_pojazdu = models.ForeignKey(Pojazdy, models.DO_NOTHING, db_column="id_pojazdu")

    class Meta:
        managed = False
        db_table = "zadania_pojazdy"
        unique_together = (("id_zadania", "id_pojazdu"),)


class BadaniaPojazdy(models.Model):
    id_badania = models.OneToOneField(
        Badania, models.DO_NOTHING, db_column="id_badania", primary_key=True
    )
    id_pojazdu = models.ForeignKey("Pojazdy", models.DO_NOTHING, db_column="id_pojazdu")

    class Meta:
        managed = False
        db_table = "badania_pojazdy"
        unique_together = (("id_badania", "id_pojazdu"),)


class BadaniaWydarzenia(models.Model):
    id_badania = models.OneToOneField(
        Badania, models.DO_NOTHING, db_column="id_badania", primary_key=True
    )
    id_wydarzenia = models.ForeignKey(
        "Wydarzenia", models.DO_NOTHING, db_column="id_wydarzenia"
    )

    class Meta:
        managed = False
        db_table = "badania_wydarzenia"
        unique_together = (("id_badania", "id_wydarzenia"),)


class WydarzeniaZadania(models.Model):
    id_wydarzenia = models.OneToOneField(
        Wydarzenia, models.DO_NOTHING, db_column="id_wydarzenia", primary_key=True
    )
    id_zadania = models.ForeignKey("Zadania", models.DO_NOTHING, db_column="id_zadania")

    class Meta:
        managed = False
        db_table = "wydarzenia_zadania"
        unique_together = (("id_wydarzenia", "id_zadania"),)
