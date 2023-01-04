from django.db import models

# Create your models here.
class Pomieszczenia(models.Model):
    nr_pomieszczenia = models.BigIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32)
    opis = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "pomieszczenia"
