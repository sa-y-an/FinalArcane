from django.urls import path, include
from . import views

app_name = 'home'


urlpatterns = [
    path('', views.home, name='home'),
    path('rules/', views.rules, name="rules"),
    path('abadakadabra/qualifiedlist/', views.page, name="page"),
    path('drstrange123emails/', views.email_users, name="player")
]
