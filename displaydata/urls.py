from django.urls import path
from . import views

app_name = 'displaydata'

urlpatterns = [
    path('', views.categoryChoice, name = 'category'),
    path('<slug:category_name_slug>/displaydata', views.displayData, name = 'displaydata'),
    path('displaydata', views.displayData, name = 'displaydata'),
    path('load_counties', views.load_counties, name ='ajax_load_counties'),
    path('<slug:category_name_slug>/create_linegraph/', views.create_linegraph, name= 'create_linegraph'),
    path('<slug:category_name_slug>/create_bargraph/', views.create_bargraph, name= 'create_bargraph'),
    path('export/', views.export, name= 'export'),
]