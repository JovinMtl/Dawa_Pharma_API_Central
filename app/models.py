from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Pharma(models.Model):
    name_pharma = models.CharField(max_length=35, default="Pharma")
    code_pharma = models.CharField(max_length=8, default="PH000")
    loc_street = models.CharField(max_length=15, default="13")
    loc_quarter = models.CharField(max_length=15, default="Kamenge")
    loc_commune = models.CharField(max_length=15, default="Ntahangwa")
    loc_Province = models.CharField(max_length=15, default="Bujumbura")
    loc_country = models.CharField(max_length=15, default="Burundi")
    ranking = models.IntegerField(default=0)
    joined_on = models.DateTimeField(default=timezone.now)
    last_connected = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Pharmacie"


class User(User):
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE)


class MedCollection(models.Model):
    nom_med = models.CharField(max_length=75, default="med")
    qte = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_per = models.DateField(default=timezone.now)