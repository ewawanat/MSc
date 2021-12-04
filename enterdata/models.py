from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from datetime import date
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True) 
    slug = models.SlugField(unique=True)

    #to make the url dynamic to query the form based on the chosen category: 
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.full_clean()
        super(Category, self).save(args, **kwargs)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)
    class Meta: 
        ordering = ['name']

    def __str__(self):
        return self.name
    
class County(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    in_country = models.ForeignKey(Country, default=1, max_length=50, on_delete=CASCADE)
    #postcode = models.CharField(max_length=50, blank = True)

    class Meta: 
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Species(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=PROTECT)    
    class Meta: 
        ordering = ['name']

    def __str__(self): 
        return self.name  #function to return the name of the instance of Species
        
class Sighting(models.Model):
    species = models.ForeignKey(Species, default=None, on_delete=PROTECT)
    date_seen = models.DateField(default=date.today)
    photo = models.ImageField(default ='default.png', blank = True)
        # def __str__ self.
    in_country = models.ForeignKey(Country, default = None, on_delete = PROTECT)
    in_county = models.ForeignKey(County, default = None, on_delete = CASCADE)
    #sound_file = models.FileField(upload_to=/'sounds/')
    #class Meta:
    # db_table='Audio_store'
    #maybe later add user 
    user = models.ForeignKey(User, default = None, on_delete = PROTECT)

    def __str__(self): 
        return self.species.name  #function to return the name of the instance of Species