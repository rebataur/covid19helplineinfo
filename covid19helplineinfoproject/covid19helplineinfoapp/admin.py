from django.contrib import admin

# Register your models here.
from .models import LocalHelpInfo, News,  Dashboard,LoadDataModel

admin.site.register(LocalHelpInfo)

admin.site.register(News)

admin.site.register(Dashboard)

admin.site.register(LoadDataModel)