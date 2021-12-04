from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from enterdata.models import Country, County, Species



class DisplayForm(models.Model):
    
    # species_set = species_name.objects.values_list('name')
   # species_name = models.ForeignKey(Species, on_delete=PROTECT)
   # MultiSelectField(Species, choices = SPECIES_CHOICES, on_delete=PROTECT)
    species_name = models.ManyToManyField(Species)
    in_country = models.ManyToManyField(Country)
    in_county = models.ManyToManyField(County)
    from_date = models.DateField()
    to_date = models.DateField()
    user = models.ForeignKey(User, on_delete=PROTECT, default=None)

    def __str__(self): 
        return self.species_name  #function to return the name of the instance of DisplayForm