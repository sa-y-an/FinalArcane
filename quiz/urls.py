from django.urls import path
from django.conf.urls import url,include
from . import views

app_name = 'quiz'


urlpatterns = [
    path('', views.StageOne, name='stageone'),
    path('answer/', views.Stage1Answer, name="answer"),
    path('hint/', views.Stage1Hint, name="hint"),
    path('stage2/', views.Index, name="index"),
    path('<int:qid>', views.Individual, name="individual"),
    path('passcode/', views.Passcode, name="passcode"),
    path('algo/', views.Algo, name="algo"),

]
