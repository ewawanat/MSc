from django.contrib import admin
from .models import Sighting, Species, Country, County, Category

@admin.register(Species) #registering the species model on the admin site
class SpeciesAdmin(admin.ModelAdmin):
    name = ('name', 'id', 'category')
    ordering = ('name',)

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'in_country', 'pk')
    ordering = ('in_country',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('id',)


@admin.register(Sighting)
class SightingAdmin(admin.ModelAdmin):
    list_display = ('species', 'id', 'in_country', 'in_county')
    ordering = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

