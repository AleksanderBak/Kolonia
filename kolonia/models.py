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
