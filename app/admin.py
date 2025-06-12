from django.contrib import admin

# Register your models here.
from .models import Pharma, MedCollection


admin.site.register(Pharma)
admin.site.register(MedCollection)
