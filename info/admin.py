from django.contrib import admin

# Register your models here.
import models


for m in models.infomodels:
    admin.site.register(m)
