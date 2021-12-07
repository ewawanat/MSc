from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('enterdata/', include('enterdata.urls')),
    path('displaydata/', include('displaydata.urls')),
    path('category/<slug:category_name_slug>', views.categoryChoice, name = 'category'),
    path('', views.homePage),
    path('index/', views.homePage, name = 'homepage'),
]

urlpatterns += staticfiles_urlpatterns()