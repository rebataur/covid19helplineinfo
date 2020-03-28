"""smartassetmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'covid19helplineinfoapp'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('getpeoplearound/', views.get_people_around_my_area, name='get_people_around_my_area'),
    path('persondetails', views.person_details, name='persondetails'),
    path('mylocalinfofilter',views.mylocalinfofilter,name='mylocalinfofilter'),
    path('mylocalinfo/', views.mylocalinfo, name='mylocalinfo'),
    path('mylocalinfoform/', views.mylocalinfoform, name='mylocalinfoform'),
    path('loaddata/', views.loaddata,name="loaddata"),
    path('signup/', views.signup, name='signup'),

    path('signup/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
