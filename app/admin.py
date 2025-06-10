from django.contrib import admin

# Register your models here.
from .models import User, Pharma, MedCollection


admin.site.register(User)
admin.site.register(Pharma)
admin.site.register(MedCollection)
