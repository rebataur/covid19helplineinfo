from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from django.contrib.postgres.fields import JSONField
from django.db import models

import json
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    profile_pic = models.ImageField(
        upload_to="profile_pics/",
        default="/media/profile_pics/placeholder_profile_pic.png",
    )

    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zip_code = models.IntegerField(blank=True, default=0, null=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username



class LocalHelpInfo(models.Model):
    # address = models.CharField(max_length=300, blank=True)
    # area = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=30, )
    state = models.CharField(max_length=30, )
    country = models.CharField(max_length=30, )
    zip_code = models.IntegerField(blank=True, default=0, null=True)

    helpline_phonenumber1 =  models.CharField(max_length=300,)
    helpline_phonenumber2 =  models.CharField(max_length=300, blank=True)
    helpline_phonenumber3 =  models.CharField(max_length=300, blank=True)
    helpline_whatsapp_phonenumber =  models.CharField(max_length=300, blank=True)
    helpline_email = models.CharField(max_length=300, blank=True)
    helpline_centre_address = models.TextField(max_length=300, blank=True)

    howto_get_there =  models.TextField(max_length=1024*10, blank=True)
    other_instructions = models.TextField(max_length=1024*10, blank=True)
    map_location_url = models.TextField(max_length=1024*10, blank=True)
  
    info_source  = models.TextField(blank=True)

    class Meta:
        unique_together = ('city', 'state','country',)

    @property
    def upvoted_count(self):
        return HelpInfoUpvote.objects.filter(belongs_to_helpinfo=self.id).count()

    @property
    def upvote(self, upvote_ipaddress):
        HelpInfoUpvote.objects.create(belongs_to_helpinfo=self,upvote_ipaddress=upvote_ipaddress)

class HelpInfoUpvote(models.Model):
    belongs_to_helpinfo = models.ForeignKey('LocalHelpInfo',on_delete=models.DO_NOTHING)
    upvote_ipaddress = models.CharField(max_length=30,unique=True)



def get_location_data(country,state):
    value = None
    code = None
    if country is None:
        code = 'country'
        value = LocalHelpInfo.objects.all().values('country').distinct()
    elif state is None:
        code = 'state'
        value = LocalHelpInfo.objects.filter(country=country).values('state').distinct()
    else:
        code = 'city'
        value = LocalHelpInfo.objects.filter(state=state).values('city').distinct()
    return {'location' : code, 'result': value}


class Dashboard(models.Model):
    total_cases = models.IntegerField(blank=True, default=0, null=True)
    total_recovered = models.IntegerField(blank=True, default=0, null=True)
    total_death = models.IntegerField(blank=True, default=0, null=True)
    total_ongoing = models.IntegerField(blank=True, default=0, null=True)
    important_message=  models.TextField(max_length=1024*10, blank=True) 
    
class News(models.Model):
    news =  models.TextField(max_length=1024*10, blank=True) 
    link =  models.TextField(max_length=1024*10, blank=True)