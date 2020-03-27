import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.models import BaseInlineFormSet, inlineformset_factory

from django.forms import ModelChoiceField
from .models import Profile, LocalHelpInfo, HELP_TYPE

class SignUpForm(UserCreationForm):
    help_type = forms.ChoiceField(
        required=False,
      
        choices=HELP_TYPE
    )
   
    first_name = forms.CharField(max_length=30, required=True, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Optional.")
    email = forms.EmailField(
        max_length=254, help_text="Required a valid email address."
    )
    # birth_date = forms.DateField(help_text="Required. Format: YYYY-MM-DD")
  
    lng = forms.DecimalField()
    lat = forms.DecimalField()
    district = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    address = forms.CharField()
    help_text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = User
        fields = (
            "help_type",
            "help_text",
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


CATEGORIES = (
    ("IST", "Indian Standard Time"),
    ("CET", "Central European Time"),
    ("GMT", "Greenwich Meridian Time"),
    ("UTC", "Coordinated Universal Time"),
)


class ProfileForm(forms.ModelForm):
    time_zone = forms.ChoiceField(
        initial="CAR",
        label="Time Zone",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=CATEGORIES,
    )

    class Meta:
        model = Profile
        fields = ( "city","state", "country", "zip_code", "bio", "profile_pic")


class LocalHelpInfoForm(forms.ModelForm):
  

    class Meta:
        model = LocalHelpInfo
        fields = ('city' ,    'state' ,    'country' ,    'zip_code',    'helpline_phonenumber1',    'helpline_phonenumber2' ,    'helpline_phonenumber3',    'helpline_whatsapp_phonenumber',    'helpline_email',    'helpline_centre_address',    'howto_get_there',   'other_instructions' ,    'map_location_url',    'info_source' 
)
