from django.urls import path
from . import views

app_name = 'displaydata'

urlpatterns = [
    path('displaydata', views.displayData, name = 'displaydata'),
    path('load_counties', views.load_counties, name ='ajax_load_counties'),
    path('create_linegraph/', views.create_linegraph, name= 'create_linegraph'),
    path('create_bargraph/', views.create_bargraph, name= 'create_bargraph'),
    path('export/', views.export, name= 'export'),
]