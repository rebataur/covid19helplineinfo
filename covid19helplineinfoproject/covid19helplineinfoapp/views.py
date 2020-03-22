import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Q

from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth
from django.db.models import Avg, Count, Min, Sum

# from .models import

from .forms import SignUpForm, ProfileForm, LocalHelpInfoForm


from .models import (
    Profile,
    LocalHelpInfo,
    News,
    Dashboard,
    LoadDataModel,

    get_location_data

)



def index(request):
    return render(request,'covid19helplineinfoapp/index.html',context={})

def home(request):
    context = {
        'local_help_circle' : True,
        'my_local_area_selected' : True
    }

    news = News.objects.all()

    dashboard = Dashboard.objects.all()[0] if len(Dashboard.objects.all()) > 0 else None
    context['news'] = news
    context['dashboard'] = dashboard

    return render(request,'covid19helplineinfoapp/home.html',context=context)


def mylocalinfo(request):
    country = request.GET.get('country')
    state = request.GET.get('state')
    # city = request.GET.get('city')
    print('==========')
    print(country,state)
    if country and state :       
        print('country found',request.GET.get('country'))
        info = LocalHelpInfo.objects.filter(country=country,state=state)[0]
        context = {'info' : info }
        return render(request,'covid19helplineinfoapp/mylocalinfodetail.html',context=context)

    context = {
        'local_help_circle' : True,
        'my_local_area_selected' : True
    }

    result = get_location_data(None,None)
    print(result)
    context[result['location']] = result['result']


    return render(request,'covid19helplineinfoapp/mylocalinfo.html',context=context)


def mylocalinfofilter(request):

    if request.method == 'POST':
        country = request.POST.get('country')
        state = request.POST.get('state')
        # city = request.POST.get('city')
        location_data = get_location_data(country,state)
        print(location_data)
        options ='<option>Select One</option>'
        
        if request.POST.get('state'):
            res = location_data['result']
            for r in res:
                print(res)
                options += '<option value="{}">{}</option>'.format(r['city'],r['city'])
            return HttpResponse(options)
        elif request.POST.get('country'):
            res = location_data['result']
            for r in res:
                print(res)
                options += '<option value="{}">{}</option>'.format(r['state'],r['state'])
            return HttpResponse(options)
      

    context = {
        'local_help_circle' : True,
        'my_local_area_selected' : True
    }

    result = get_location_data(None,None,None)
    print(result)
    context[result['location']] = result['result']


    return render(request,'covid19helplineinfoapp/mylocalinfo.html',context=context)


def mylocalinfoform(request):
    print("submitting form")
    if request.method == 'POST':
        print("submitting form")
        form = LocalHelpInfoForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {}
    context['form'] = LocalHelpInfoForm()

    return render(request,'covid19helplineinfoapp/mylocalinfoform.html',context=context)
import io
def loaddata(request):
    loaddata = LoadDataModel.objects.all()[0]
    # print(loaddata.data)
    f = io.StringIO(loaddata.data)
    for line in f:
        # print(line.splitlines())
        val = line.splitlines()[0].split(',')
        print(val)
        state = val[0]
        phonenumber1 = val[1]        
        phonenumber2 = val[2] if len(val) == 3 else '+91-11-23978046'
        phonenumber3 = '+91-11-23978046' if len(val) == 3 else '' 
        LocalHelpInfo.objects.create(city='NA', country='India',state=state,helpline_phonenumber1=phonenumber1,helpline_phonenumber2=phonenumber2,helpline_phonenumber3=phonenumber3)
    return HttpResponse(200)
# ======================== END OF BIZ FUNCTIONALITY======================


@login_required
def profile(request):
    profile_instance = Profile.objects.filter(user__username=request.user)[0]
    context = {
        "username": request.user,
        "profile_pic_url": profile_instance.profile_pic.url,
    }
    return render(request, "covid19helplineinfoapp/profile.html", context)


@login_required
def help(request):
    profile_instance = Profile.objects.filter(user__username=request.user)[0]
    context = {
        "username": request.user,
        "profile_pic_url": profile_instance.profile_pic.url,
    }
    return render(request, "covid19helplineinfoapp/help.html", context)


######################################################
######################################################
######################################################

#                  Authentication

######################################################
######################################################
######################################################
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                user = form.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = "Activate Your MySite Account"
                message = render_to_string(
                    "registration/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        "token": account_activation_token.make_token(user),
                    },
                )
                print("=============")
                print(user.pk)
                # print(urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'))
                print(message)
                print(user.email)

                # user.email_user(subject, message)

                # ----------------
                email = EmailMessage(subject, message, to=[user.email])
                email.send()
                return redirect("account_activation_sent/")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
        print(token)
        print(account_activation_token.check_token(user, token))
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            print(user)
            login(request, user)
            return redirect("/")
        else:
            print("invalid")
            return render(request, "registration/account_activation_invalid.html")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


def account_activation_sent(request):
    return render(request, "registration/account_activation_sent.html")


def error_404(request, exception):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)


def error_500(request):
    data = {}
    return render(request, "registration/account_activation_sent.html", data)

