from django.contrib import admin

# Register your models here.
from .models import LocalHelpInfo, News,  Dashboard

admin.site.register(LocalHelpInfo)

admin.site.register(News)

admin.site.register(Dashboard)