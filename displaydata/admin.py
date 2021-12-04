from django.contrib import admin

from displaydata.models import DisplayForm

# Register your models here.
@admin.register(DisplayForm) #registering the species model on the admin site
class DisplayFormAdmin(admin.ModelAdmin):
    name = ('species_name', 'id')
    ordering = ('species_name',)