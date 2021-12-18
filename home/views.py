from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from user.views import leaderboard
from .models import Leaders
from user.models import Player
from quiz.forms import UserAnswer
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.admin.views.decorators import staff_member_required

from django.core.mail import send_mass_mail
from django.core import mail

# Create your views here.
@staff_member_required
def email_users(request) :
    player = Player.objects.all()
    return render(request, 'home/emails.html', {'players':player})


def not_logged_in(user):
    return not user.is_authenticated


def base(request):
    return render(request, 'home/base.html')


def home(request):
    return render(request, 'home/home.html')


def hello(request):
    return render(request, 'home/hello.html')


def rules(request):
    return render(request, 'home/rule.html')


def error_404(request, exception):
        data = {}
        return render(request,'home/404.html', data)


def send_mass_qualification_mails(leaderboard):
    '''Mass email alternative '''

    subject = "You have Qualified for Round 2" 
    with open('text_messages/login_user.txt', 'r') as file:
        message = file.read()
    message = str(message)
    from_email = "ieeesbnitd@gmail.com"
    recipient_list = list(leaderboard.values_list('email', flat=True))

    messages = [(subject, message, from_email, [recipient]) for recipient in recipient_list]

    return send_mass_mail(messages,fail_silently=True)




def send_qualification_mails(leaderboard) :
    '''Helper method to send qualification emails
    This is currently using cc and doesnot use mass mailing features
    Have to replace it.    
    '''

    with open('text_messages/login_user.txt', 'r') as file:
        message = file.read()


    subject = "You have Qualified for Round 2" 
    message = str(message)
    from_email = "ieeesbnitd@gmail.com"
    reciever_list = list(leaderboard.values_list('email', flat=True))
        
    connection = mail.get_connection()
    connection.open()
    email1 = mail.EmailMessage(subject, message, from_email,
                            reciever_list, connection=connection)
    email1.send()
    connection.close()





@staff_member_required
def page(request):
    '''Only After 1st Round is complete
    SQL Querries = 2 ( generally )
    Update Querry = 1
    '''

    cutOffScore = Leaders.objects.all()[0].cutoffScore
    leaderboard = Player.objects.filter(score__gte = cutOffScore )
    form = UserAnswer

    context = {  
    "leaders" : leaderboard  ,
    "form" : form ,
    "case" : 0,
    "cutOffScore" : cutOffScore
    }



    if request.method == "GET" :
        return render(request, "home/page.html",context= context )

    if request.method == "POST":

        my_form = UserAnswer(request.POST)

        if my_form.is_valid():


            ans = my_form.cleaned_data.get("answer")
            organs = "AlohaMoraHarryPotter"

            # if the answer is correct
            if (str(organs) == str(ans)):   
                Player.objects.filter(score__gte = cutOffScore).update(level2 = 0 )
                context["case"] = 1

                numberSend = send_mass_qualification_mails(leaderboard)
                context["numberSend"] = numberSend

                return render(request, "home/page.html",context= context )

            # incorrect answer
            else:   
                context["case"] = 2
                return render(request, "home/page.html",context= context )
                
        else:
            return HttpResponse('<h2> Your Form Data was Invalid </h2>')







