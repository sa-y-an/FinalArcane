from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
import user
import home

handler404 = 'home.views.error_404'


urlpatterns = [
    path('harrypotter/', admin.site.urls),
    path('user/', include('user.urls')),
    path('quiz/', include('quiz.urls')),
    path('', include('home.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', user.views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
