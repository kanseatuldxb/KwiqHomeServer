from django.contrib import admin
from .models import Project, Unit, Area, Units, GovernmentalArea, Image

# Register your models here.
admin.site.register(Project)
admin.site.register(Unit)
admin.site.register(Area)
admin.site.register(Units)
admin.site.register(GovernmentalArea)
admin.site.register(Image)
