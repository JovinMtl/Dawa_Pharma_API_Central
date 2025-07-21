from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def first_user():
    user = User.objects.first()
    return user



# Create your models here.

class Pharma(models.Model):
    name_pharma = models.CharField(max_length=35, default="Pharma", unique=True)
    code_pharma = models.IntegerField(default=1000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=first_user)
    tel = models.IntegerField(default=0)
    loc_street = models.CharField(max_length=15, default="13")
    loc_quarter = models.CharField(max_length=15, default="Kamenge")
    loc_commune = models.CharField(max_length=15, default="Ntahangwa")
    loc_Province = models.CharField(max_length=15, default="Bujumbura")
    loc_country = models.CharField(max_length=15, default="Burundi")
    score = models.IntegerField(default=0)
    joined_on = models.DateTimeField(default=timezone.now)
    last_connected = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.name_pharma}"
    class Meta:
        verbose_name = "Pharmacie"

def first_pharma():
    pharma = Pharma.objects.first()
    return pharma

class MedCollection(models.Model):
    nom_med = models.CharField(max_length=75, default="med")
    qte = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    owner = models.ForeignKey(Pharma, on_delete=models.CASCADE, default=first_pharma)
    date_per = models.CharField(max_length=35, default="2028")
    sync_code = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{(self.nom_med)[:10]}, {self.price}: {self.owner}"