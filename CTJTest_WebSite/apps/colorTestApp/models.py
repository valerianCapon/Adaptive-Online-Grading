from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from colorfield.fields import ColorField
from collections import namedtuple


COLOR_VALIDATOR = [MinValueValidator(0), MaxValueValidator(255)]

class ColorSetAssmt(models.Model):
    # ------------------------Identity of the Color Test --------------------------------
    # name = "DateStart + Type + Judge
    name = models.CharField(primary_key=True, max_length=200, unique=True)
    type = models.CharField(
        max_length=1,
        choices=(
        ('r', 'Rubric'),
        ('a', 'ACJ'),
        ('t', 'CTJ'),
        ),
        default='r',
    )
    judge = models.OneToOneField(User, on_delete=models.CASCADE, related_name="is_User")
    
    #auto_now_add=True mean the date is saved when the object is created only
    date_started = models.DateTimeField(auto_now_add=True) 
    #auto_now=True mean the date is saved everytime the object is saved 
    date_ended = models.DateTimeField(blank=True, null=True)

    # ------------------------Atributes meant for computing --------------------------------

    # Must be the summation of test's assessments' duration
    # not the dates of ColorSetAssment
    duration = models.DurationField(blank=True, null=True)
    
    nb_of_assmnt = models.SmallIntegerField(validators=[MinValueValidator(limit_value=0)], default=0 )
    nb_of_assmnt_max = models.SmallIntegerField(validators=[MinValueValidator(limit_value=0)], default=0 )


    def __str__(self) -> str:
        return self.name
    


class Color(models.Model):
    name = models.CharField(primary_key=True, max_length=25, unique=True)
    color_code = ColorField(unique=True)

    def __str__(self) -> str:
        return self.name

    """ Return the rgb values of the hex color in a named tuple 
        ex: rgb_tuple = color1.rgb_values()
            red = rgb_tuble.red                                 """
    def rgb_values(self) -> tuple:
        rgb_tuple = namedtuple( 'rgb', ['red', 'blue', 'green'])
        return rgb_tuple(red=int("0x" + self.color_code[0:1]),
                         blue=int("0x" + self.color_code[2:3]),
                         green=int("0x" + self.color_code[4:5]) )


# Rubric Assessment
class ColorRubricAssmt(models.Model):
    # name = test.name + color
    name = models.CharField(primary_key=True, max_length=100, unique=True)
   
    color_set_assmt = models.ForeignKey(ColorSetAssmt, on_delete=models.CASCADE, related_name="of_ColorSetAssmt")
    

    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    shade_guessed = models.SmallIntegerField(blank=True, null=True, validators=COLOR_VALIDATOR)

    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    




class ColorSet(models.Model):
    name = models.CharField(primary_key=True, max_length=25, unique=True)
    #Useless to set null=True cause it's never set to NULL in the database
    description = models.TextField(max_length=200, blank=True) 

    colors = models.ManyToManyField(Color)
    quantityOfColors = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0)


    def __str__(self) -> str:
        return self.name

