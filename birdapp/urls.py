from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from graphene_django import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('enterdata/', include('enterdata.urls')),
    path('displaydata/', include('displaydata.urls')),
    path('', views.homePage),
    path('index/', views.homePage, name = 'homepage'),
]

urlpatterns += staticfiles_urlpatterns()