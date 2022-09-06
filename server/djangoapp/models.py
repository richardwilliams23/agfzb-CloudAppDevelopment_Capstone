from django.db import models
from django.utils.timezone import now




# Create your models here.


# Models subclassed from Django Model...

# E.g. Audi, BMW, Ford.
class CarMake(models.Model):
    id = models.IntegerField( primary_key=True )
    name = models.CharField( null=False, max_length=50 )
    description = models.CharField( null=True, max_length=100 )
    def __str__(self):
        return self.name

# E.g. S4, S6, S8, 7-series.
class CarModel(models.Model):
    id = models.IntegerField( primary_key=True )
    make = models.ForeignKey( CarMake, null=False, on_delete=models.CASCADE)
    name = models.CharField( null=False, max_length=50 )
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )
    year = models.DateField(default=now)

    def __str__(self):
        return str(self.make) + ", " + \
               self.name + ", " + \
               self.type + ", " + \
               str(self.year)


# Plain Python classes used as a plain data objects 
# for storing objects returned from Cloudant...

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__( self, dealership, name, purchase, review ):

        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review

        self.id = ""
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""
        self.sentiment = ""

    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review




