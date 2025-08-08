from django.contrib import admin
from .models import Client, FollowUp, SearchFilter, Feedback

# Register your models here.
admin.site.register(Client)
admin.site.register(SearchFilter)
admin.site.register(FollowUp)
admin.site.register(Feedback)
