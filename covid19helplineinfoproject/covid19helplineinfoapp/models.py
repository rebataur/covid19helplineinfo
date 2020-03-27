from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from django.contrib.postgres.fields import JSONField
# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry

import json
from datetime import datetime

HELP_TYPE = (
    ('SEEKING_HELP','Seeking Help'),
    ('VOLUNTEER', 'Volunteer')
)
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
    location = models.PointField(null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6,default=0.0)
    lng = models.DecimalField(max_digits=10, decimal_places=6,default=0.0)

    address = models.CharField(max_length=300, blank=True)
    district = models.CharField(max_length=30, blank=True)    
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zip_code = models.IntegerField(blank=True, default=0, null=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)

    help_type = models.CharField(max_length=30, choices=HELP_TYPE,null=True)
    help_text = models.TextField(null=True)

    def set_location(self):
        self.location=Point(int(self.lng), int(self.lat), srid=4326)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


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

class LoadDataModel(models.Model):
    data = models.TextField()


from django.db import connection

def get_people_around(id):
    with connection.cursor() as cursor:
        sql = '''
        drop view if exists distance_view;
        create or replace view distance_view as 
        SELECT p1.id as source_id,p1.lng as source_lng, p1.lat as source_lat,
               p2.id as target_id,p2.lng as target_lng, p2.lat as target_lat,
        ST_Distance(
              ST_Point(p1.lat,p1.lng)::geography,
              ST_Point(p2.lat,p2.lng)::geography
        ) as distance

        FROM covid19helplineinfoapp_profile as p1, covid19helplineinfoapp_profile as p2
        WHERE p1.id <> p2.id  
        '''
        cursor.execute(sql)

        sql = '''

        select target_id,target_lat,target_lng from distance_view where source_id = {} order by distance limit 100
        '''.format(id)
        cursor.execute(sql)
        rows = cursor.fetchall()

    return rows