from django.http import HttpResponse, HttpResponseNotFound
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Stage_1, StageTwo
from django.contrib.auth.decorators import login_required
from user.models import Player, Solved, StageOneHint
from .forms import UserAnswer
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.

value = False
hintValue = False
hintButton = True
question1 = Stage_1.objects.all()

# time variables

now = datetime.utcnow()+timedelta(hours=5.5)


# Set the Date Time Here

''' Set the date time as class datetime.datetime
    (year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)'''


#Start
quiz = datetime(2021, 10, 23, 19, 0, 0)       
# First Round Ends
firstend = datetime(2022, 10, 24, 19, 0, 0)
# Second Round Ends
end = datetime(2022, 10, 25, 23, 59, 59)



@login_required(login_url='/login/auth0', redirect_field_name=None)
def Algo(request):
    if request.method == "POST":
        player = get_object_or_404(Player, user=request.user)
        n = player.question_level
        if n > Stage_1.objects.count():
            question = Stage_1.objects.order_by('-level')
            return render(request, 'quiz/algorithm.html', {"questions": question})
        else:
            raise Http404("Page does not exist")
    else:
        raise Http404("Page does not exist")


@login_required(login_url='/login/auth0', redirect_field_name=None)
def StageOne(request):
    ''' Set the date time as class datetime.datetime
    (year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)'''

    # sanity check
    try : 
        player = get_object_or_404(Player, user=request.user)
    except Player.DoesNotExist: 
        return redirect('user:psave')
  

    # print(now)
    if now < quiz:
        print('not time ' + str(quiz))
        return render(request, 'quiz/timer2.html')
    
    # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})

    # this is for first round ends but couldnt make to round 2
    if firstend < now and player.level2 < 0:
        return render(request, 'quiz/disqualified.html')

    

    else:
        print('quiz on')
        if player.level2 < -1:
            player = get_object_or_404(Player, user=request.user)
            question_level = player.question_level

            if player.question_level > Stage_1.objects.count():
                formp = UserAnswer
                check = False
                return render(request, 'quiz/end.html', {"form": formp, "check": check})

            question = get_object_or_404(Stage_1, level=int(question_level))
            my_form = UserAnswer
            hall = player.stageonehint_set.all()
            for i in hall:
                if i.level == question_level:
                    return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form, "value": value, "hint": i.taken})
            player.stageonehint_set.create(
                level=int(question_level), taken=False)
            hint = player.stageonehint_set.get(level=int(question_level))
            return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form, "value": value, "hint": hint.taken})

        if player.level2 == -1:
            return render(request, 'quiz/wait.html')

        if player.level2 > -1:
            q = StageTwo.objects.all()
            player = get_object_or_404(Player, user=request.user)
            if (player.count2 < StageTwo.objects.count()):
                return render(request, 'quiz/stage2index.html', {"q": q, "player": player})
            else:
                return render(request, 'quiz/finish.html', {"player": player})


@login_required(login_url='/login/auth0', redirect_field_name=None)
def Stage1Hint(request):
    # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})

    player = get_object_or_404(Player, user=request.user)
    hint = player.stageonehint_set.get(level=int(player.question_level))
    my_form = UserAnswer
    if hint.taken == True:
        question_level = player.question_level
        question = get_object_or_404(Stage_1, level=int(question_level))
        return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form, "value": value, "hint": hint.taken})
    else:
        player.score -= 5
        hint.taken = True
        hint.save()
        player.save()
        question_level = player.question_level
        question = get_object_or_404(Stage_1, level=int(question_level))
        return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form, "value": value, "hint": hint.taken})


@login_required(login_url='/login/auth0', redirect_field_name=None)
def Stage1Answer(request):

        # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})


    if request.method == "POST":
        player = get_object_or_404(Player, user=request.user)
        question_level = player.question_level

        try:
            question = Stage_1.objects.get(level=int(question_level))
        except Stage_1.DoesNotExist:
            formp = UserAnswer
            check = False
            return render(request, 'quiz/end.html', {"form": formp, "check": check})

        my_form = UserAnswer(request.POST)

        if my_form.is_valid():

            ans = my_form.cleaned_data.get("answer")

            if (str(ans).lower() == str(question.answer).lower()):  # stage one answer checking
                value = False
                player.score += 15
                player.last_submit = timezone.now()
                player.question_level += 1

                player.save()
                question_level = player.question_level
                try:
                    question = Stage_1.objects.get(
                        level=int(question_level))
                except Stage_1.DoesNotExist:
                    formp = UserAnswer
                    check = False
                    return render(request, 'quiz/end.html', {"form": formp, "check": check})

                if player.question_level > Stage_1.objects.count():
                    formp = UserAnswer
                    check = False
                    return render(request, 'quiz/end.html', {"form": formp, "check": check})
                else:
                    my_form1 = UserAnswer
                    player.stageonehint_set.create(
                        level=int(question_level), taken=False)
                    hint = player.stageonehint_set.get(
                        level=int(question_level))
                    if ((question_level) - 1 > 0):
                        try:
                            delobj = player.stageonehint_set.get(
                                level=int(int(question_level)-1))
                        except player.stageonehint_set.DoesNotExist:
                            print("object doesnot exit")
                        else:
                            e = delobj.delete()
                            print(e)

                    return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form1, "value": value, "hint": hint.taken})

            else:
                my_form1 = UserAnswer
                value = True
                hint = player.stageonehint_set.get(
                    level=int(question_level))
                return render(request, 'quiz/Stage1.html', {"question": question, "form": my_form1, "value": value, "hint": hint.taken})
        else:
            return HttpResponse('<h2> Form data not valid</h2>')

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/login/auth0', redirect_field_name=None)
def Index(request):

    # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})


    q = StageTwo.objects.order_by('level')
    player = get_object_or_404(Player, user=request.user)
    if(player.level2 < -1):
        return render(request, 'quiz/smart.html')
    elif(player.level2 == -1):
        return render(request, 'quiz/wait.html')
    else:
        if (player.count2 < StageTwo.objects.count()):
            return render(request, 'quiz/stage2index.html', {"q": q, "player": player})
        else:
            return render(request, 'quiz/finish.html', {"player": player})


@login_required(login_url='/login/auth0', redirect_field_name=None)
def Passcode(request):


    # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})


    code = "ENIGMAHACK"
    if request.method == "POST":
        my_form = UserAnswer(request.POST)
        if my_form.is_valid():
            # print(my_form.cleaned_data)
            ans = my_form.cleaned_data.get("answer")

            if (str(ans).lower() == str(code).lower()):
                player = get_object_or_404(Player, user=request.user)
                player.level2 = -1
                player.score += 40
                player.last_submit = timezone.now()
                player.save()
                question_level = player.question_level
                if ((question_level) - 1 > 0):
                    try:
                        delobj = player.stageonehint_set.get(
                            level=int(int(question_level)-1))
                    except:
                        print("object doesnot exit")
                    else:
                        e = delobj.delete()
                        print(e)
                # print(player.level2)
                q = StageTwo.objects.all()
                player = get_object_or_404(Player, user=request.user)
                return render(request, "quiz/wait.html", {"q": q, "player": player})
            else:
                check = True
                formp = UserAnswer
                return render(request, "quiz/end.html", {"check": check, "form": formp})
        else:
            return HttpResponse("<h1>form data invalid </h1>")


# individual questions of stage 2
@login_required(login_url='/login/auth0', redirect_field_name=None)
def Individual(request, qid):
    '''View for stage 2'''

    # the end of the quiz
    if (now > end):
        print('end ' + str(end))
        return render(request, 'quiz/timer.html', {"end": end})

    

    player = get_object_or_404(Player, user=request.user)
    if(player.level2 < -1):
        return render(request, 'quiz/smart.html')
    elif(player.level2 == -1):
        return render(request, 'quiz/wait.html')
    else:
        # this marks if the question is solved (and shows the popup)
        value = False
        all = StageTwo.objects.all()
        player = get_object_or_404(Player, user=request.user)
        s = player.solved_set.all()     # solved class has 2 objects 1. level_on 2. solved
        question = get_object_or_404(StageTwo, level=qid)
        p = get_object_or_404(Player, user=request.user)
        p.level2 = int(qid)
        p.save()            # sets the current level of the user to the visiting question

        flag = False        # player solved it or not
        for i in s:         # checks if player have already visited the question
            if (i.level_on == qid):
                if (i.solved == True):  # checks if player have solved the question
                    flag = True
                    # then returns the solved page
                    return render(request, 'quiz/solved.html', {"all": all})
                else:
                    flag = True
                    if request.method == "GET":     # if the player comes for the question
                        my_form = UserAnswer
                        return render(request, 'quiz/individual.html', {"question": question, "form": my_form, "value": value, "all": all})
                    if request.method == "POST":    # if the player submits the question
                        my_form = UserAnswer(request.POST)

                        if my_form.is_valid():
                            ans = my_form.cleaned_data.get("answer")
                            organs = get_object_or_404(
                                StageTwo, level=qid).answer

                            # correct answer
                            if (str(organs).lower() == str(ans).lower()):   # if the answer is correct
                                player.score += 20
                                player.last_submit = timezone.now()
                                player.count2 += 1          # count of solved questions
                                i.solved = True         # the question is set to solved corrosponding to that level
                                i.save()
                                player.save()
                                return render(request, 'quiz/solved.html', {"all": all})

                            # incorrect answer
                            else:   # returns the same question
                                value = True
                                return render(request, 'quiz/individual.html', {"question": question, "form": my_form, "value": value, "all": all})
                        else:
                            return HttpResponse('<h2> Your Form Data was Invalid </h2>')
                            # invalid form data submitted by tampering with developer console

        if (flag == False):  # the player didnot visited the question before
            # creates a Solved object with level_on = question level and solved set to False
            player.solved_set.create(level_on=qid, solved=False)

            if request.method == "GET":
                my_form = UserAnswer
                return render(request, 'quiz/individual.html', {"question": question, "form": my_form, "all": all})
            if request.method == "POST":
                my_form = UserAnswer(request.POST)
                if my_form.is_valid():
                    ans = my_form.cleaned_data.get("answer")
                    organs = get_object_or_404(StageTwo, level=qid).answer
                    # if the player succesfully solves the question
                    if (str(organs).lower() == str(ans).lower()):
                        player.score += 5
                        player.last_submit = timezone.now()
                        player.count2 += 1          # count of solved questions
                        i = player.solved_set.get(level_on=qid)
                        i.solved = True  # sets the solved to true
                        i.save()
                        player.save()
                        return render(request, 'quiz/solved.html', {"all": all})
                    else:   # returns the same question
                        value = False
                        return render(request, 'quiz/individual.html', {"question": question, "form": my_form, "all": all})
                else:
                    return HttpResponse('<h2> Your Form data was Invalid </h2>')


