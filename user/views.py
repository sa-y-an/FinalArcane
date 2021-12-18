from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from .import models
from datetime import datetime, timedelta
from .forms import UserDetails
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


current_leaderboard = None


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY

    return_to = 'https://ieee-arcane.herokuapp.com/' # this can be current domain


    path_to_file = os.path.join(BASE_DIR, 'Qriosity/config.json')

    if( os.path.exists(path_to_file)  ) :
        return_to = 'http://127.0.0.1:8000/'

    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')



@login_required(login_url='/login', redirect_field_name=None)
def dashboard(request):
    '''Return the Dasboard of User'''

    # Sanity Check
    try : 
        player = models.Player.objects.get(user=request.user)
    except models.Player.DoesNotExist:
        return redirect('user:psave')


    print("In dashboard - Name - {}  User - {}".format(player.name, player.user))
    cl = models.Player.objects.order_by(
        '-score', 'last_submit')
    j = 0

    for i in cl:
        j += 1
        if i.user == player.user:
            print(j)
            break
    return render(request, 'user/dashboard.html', {'player': player, "rank": j})


#@login_required(login_url='/login', redirect_field_name=None)
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.last_submit = datetime.utcnow()+timedelta(hours=5.5)
            player.name = response.get('name')
            player.image = response.get('picture')
            player.email = response.get('email')
            player.save()
    elif backend.name == 'facebook':
        profile = user
        try:
            player = models.Player.objects.get(user=profile)
        except:
            player = models.Player(user=profile)
            player.name = response.get(
                'first_name')+" "+response.get('last_name')
            player.email = response.get('email')
            player.image = "http://graph.facebook.com/%s/picture?type=large" \
                % response["id"]
            player.last_submit = datetime.utcnow()+timedelta(hours=5.5)
            player.save()


# @login_required(login_url='/login', redirect_field_name=None)
def leaderboard(request):
    global current_leaderboard

    current_leaderboard = models.Player.objects.order_by(
        '-score', 'last_submit')

    leader = models.Player.objects.order_by(
        '-score', 'last_submit')[:1]

    print(type(leader[0].last_submit))

    n = models.Player.objects.count()

    return render(request, 'user/leaderboard.html', {'leaderboard': current_leaderboard, 'leader': leader, 'n': n})


def privacy_policy_fb(request):
    '''jhanter baal'''
    return render(request, "user/privacypolicy.html")


@login_required(login_url='/login', redirect_field_name=None)
def UserData(request):
    my_form = UserDetails()
    context = {
        "form": my_form
    }
    return render(request, "user/details.html", context)


@login_required(login_url='/login', redirect_field_name=None)
def Formdata(request):
    if request.method == "POST":
        my_form = UserDetails(request.POST)
        if my_form.is_valid():
            # my form is valid
            form_data = my_form.cleaned_data
            p1 = models.Player.objects.get(user=request.user)
            r = models.PlayerDetails(
                user_name=p1, college=form_data['college'], year=form_data['year'], contact=form_data['contact'],
                full_name=form_data['full_name'])
            p1.name = r.full_name
            p1.save()
            r.save()

        else:
            z = my_form.errors
            print(z)
    p1 = models.Player.objects.get(user=request.user)

    try:
        r = models.PlayerDetails.objects.get(user_name=p1)
        return render(request, 'user/form_status.html', {"details": r})
    except models.PlayerDetails.DoesNotExist:
        render(request, "user/details.html")

    my_form = UserDetails()
    context = {
        "form": my_form
    }
    return render(request, "user/details.html", context)


def story(request):
    return render(request, 'user/story.html')


@login_required
def psave(request) :
    ''' View to save profile of a person'''

    my_form = UserDetails()
    user=request.user

    auth0_user=user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture'],
        'email':user.email,
    }

    try :
        p = models.Player.objects.get(user=user)
        return redirect('home:home')
    except models.Player.DoesNotExist:

        p = models.Player.objects.create(
                user=user)
        p.last_submit = datetime.utcnow()+timedelta(hours=5.5)
        p.name = user_data['name']
        p.image = user_data['picture']
        p.email = user_data['email']
        p.save()

        messages.success(request, 'Account was created for ' + user.username)

    context = {
        "form": my_form
    }
    return render(request, "user/details.html", context)
    
def count(request) :
    p = models.Player.objects.count()
    p -= 30
    return HttpResponse("<h1> Participant Count - {} <h1>".format(p))



@staff_member_required
def checkboard(request):
    global current_leaderboard

    current_leaderboard = models.Player.objects.order_by(
        '-score', 'last_submit')

    leader = models.Player.objects.order_by(
        '-score', 'last_submit')[:1]

    print(type(leader[0].last_submit))

    n = models.Player.objects.count()

    return render(request, 'user/check.html', {'leaderboard': current_leaderboard, 'leader': leader, 'n': n})
