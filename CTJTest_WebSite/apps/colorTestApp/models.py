from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User

class ColorTest(models.Model):
    TYPE_OF_TEST = (
        ('r', 'Rubric'),
        ('a', 'ACJ'),
        ('t', 'CTJ'),
    )
    type = models.CharField(
        max_length=1,
        choices=TYPE_OF_TEST,
        blank=True,
        default='r',
    )

    judge = models.OneToOneField(User, on_delete=models.CASCADE, related_name="is_user")
    
    #auto_now_add=True mean the date is saved when the object is created only
    date_started = models.DateTimeField(auto_now_add=True) 
    #auto_now=True mean the date is saved everytime the object is saved 
    date_ended = models.DateTimeField(auto_now=True)

    duration = models.DurationField()
    
    #name = "Date + Type + Judge
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    


class Color(models.Model):
    color_code = ColorField(default='#00FF00', unique=True)
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

    

#Rubric Assessment
class RubricAssmt(models.Model):
    test = models.ForeignKey(ColorTest, on_delete=models.CASCADE, related_name="of_test")
    color = models.ForeignKey(Color)
    shade_guessed = models.IntegerField()
    time_start = models.DateField(auto_now=True)
    time_end = models.DateField(auto_now=True)

    #name = test.name + color
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name



class ColorSet(models.Model):
    colors = models.ManyToManyField(Color)
    quantityOfColors = models.IntegerField(min_value=0)
    name = 
    description = 

