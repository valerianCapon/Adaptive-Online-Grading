from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User


# class Test(models.Model):
#     type = models.CharField(max_length=8)
#     judge =
#     date_started
#     date_ended
#     duration

#     TYPE_OF_TEST = (
#         ('r', 'Rubric'),
#         ('a', 'ACJ'),
#         ('t', 'CTJ'),
#     )

#     status = models.CharField(
#         max_length=1,
#         choices=LOAN_STATUS,
#         blank=True,
#         default='m',
#         help_text='Book availability',
#     )


# class ACJAssessment(models.Model)
#     test = models.ForeignKey()
#     color = models.ForeignKey()
#     shade_guessed = 
#     time_start
#     time_end


# class ColorSet(models.Model):
#     colors = models.ManyToManyField(Color)
#     quantityOfColors = 
#     name = 
#     description = 


# class Color(models.Model):
#     color_code = ColorField(default='#00FF00')
#     color_set = models.CharField(max_length=255)
#     rank_in_set
    