from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from colorfield.fields import ColorField
from collections import namedtuple
from rubric_assessments import generate_assessments


class Color(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    color_code = ColorField(unique=True)

    def __str__(self) -> str:
        return self.name

    """
    Return the RGB values of the hex color as a named tuple
    Example: rgb_tuple = color1.rgb_values()
            red = rgb_tuple.red
    """
    def rgb_values(self) -> tuple:
        red = int(self.color_code[0:2], 16)
        blue = int(self.color_code[2:4], 16)
        green = int(self.color_code[4:6], 16)
        return namedtuple("RGB", ["red", "blue", "green"])(red=red, blue=blue, green=green)

class ColorSet(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    description = models.TextField(max_length=200, blank=True)
    colors = models.ManyToManyField(Color, blank=True, related_name='color_sets')

    def __str__(self) -> str:
        return self.name
    

class ColorSetAssessment(models.Model):
    """ name = judge_type_date """
    name = models.CharField(primary_key=True, max_length=200)
    TYPE_CHOICES = [("r", "Rubric"), ("a", "ACJ"), ("t", "CTJ")]
    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default="r",
        verbose_name="Type of the test",
    )
    color_set = models.ForeignKey(
        ColorSet, 
        on_delete=models.PROTECT, 
        related_name="assessments",
        verbose_name="Color Set",
    )
    judge = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assessed_color_sets",
        verbose_name="The user who assessed the color set",
    )
    date_started = models.DateTimeField(
        verbose_name="Start date of the test"
    )
    date_ended = models.DateTimeField(
        blank=True, null=True, verbose_name="End date of the test"
    )
    assessments_duration = models.DurationField(
        blank=True, null=True, verbose_name="Duration of assessments"
    )
    nb_of_assmnt = models.PositiveSmallIntegerField(
        default=0, verbose_name="Number of assessments done"
    )
    nb_of_assmnt_max = models.PositiveSmallIntegerField(
        default=5, verbose_name="Maximum number of assessments allowed"
    )

    class Meta:
        verbose_name_plural = "Color Set Assessments"
        get_latest_by = "date_started"
        ordering = ["date_started", "judge"]

    def __str__(self) -> str:
        return self.name
    
    def create_assmnts(self):
        generate_assessments(self)


class ColorRubricAssessment(models.Model):
    #SetAssessment's name + color's hex code
    name = models.CharField(primary_key=True, max_length=100)
    color_set_assmt = models.ForeignKey(
        ColorSetAssessment,
        on_delete=models.CASCADE,
        related_name="rubric_assessments",
    )
    color = models.ForeignKey(
        Color, on_delete=models.PROTECT, related_name="rubric_assessments"
    )
    shade_guessed = models.PositiveSmallIntegerField(
        blank=True, null=True, validators=[MaxValueValidator(255)]
    )
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Color Rubric Assessment"
        get_latest_by = "time_start"

    def __str__(self) -> str:
        return self.name

    def get_judge(self):
        return self.color_set_assmt.judge
    
    

