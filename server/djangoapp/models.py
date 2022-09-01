from django.db import models
from django.utils.timezone import now


# Create your models here.

# E.g. Audi, BMW, Ford.
class CarMake(models.Model):
    name = models.CharField( null=False, max_length=50 )
    description = models.CharField( null=True, max_length=100 )
    def __str__(self):
        return self.name

# E.g. S4, S6, S8, 7-series.
class CarModel(models.Model):

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]

    id = models.IntegerField( primary_key=True )

    make = models.ForeignKey( CarMake, null=False, on_delete=models.CASCADE)

    name = models.CharField( null=False, max_length=50 )

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




# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data

