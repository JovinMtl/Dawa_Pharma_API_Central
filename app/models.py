from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Pharma(models.Model):
    name_pharma = models.CharField(max_length=35, default="Pharma")
    code_pharma = models.CharField(max_length=8, default="PH000")
    loc_street = models.CharField(max_length=15, default="Pharma")
    loc_quarter = models.CharField(max_length=15, default="Pharma")
    loc_commune = models.CharField(max_length=15, default="Pharma")
    loc_Province = models.CharField(max_length=15, default="Pharma")
    loc_country = models.CharField(max_length=15, default="Pharma")
    ranking = models.IntegerField(default=0)
    joined_on = models.DateTimeField(default=timezone.now)
    last_connected = models.DateTimeField(default=timezone.now)


class User(User):
    pharma = models.ForeignKey(Pharma, on_delete=models.CASCADE)


class MedCollection(models.Model):
    nom_med = models.CharField(max_length=75, default="med")
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_per = models.DateField(default=timezone.now)