from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from colorfield.fields import ColorField
from collections import namedtuple
from django.db.models import F as DjangoF
from django.utils.timezone import now
from datetime import timedelta


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
    nb_of_assessement = models.PositiveSmallIntegerField(
        default=0, verbose_name="Number of assessments done"
    )
    nb_of_assessement_max = models.PositiveSmallIntegerField(
        default=5, verbose_name="Maximum number of assessments allowed"
    )

    class Meta:
        verbose_name_plural = "Color Set Assessments"
        get_latest_by = "date_started"
        ordering = ["date_started"]

    def __str__(self) -> str:
        return self.name
    
    
    def create_assessments(self):
        self.nb_of_assessement_max = self.get_nb_max_of_assessment()
        list_of_colors = self.color_set.colors.all()
        print(list_of_colors) #TODO:supr

        match self.type:
            #Rubric type of assessments
            case "r":
                self.nb_of_assessement_max = list_of_colors.count()
                for set_nb, color in zip(range(1,self.nb_of_assessement_max+1), list_of_colors):
                    print("creation of assesment nb =", set_nb," and color =",color.name) #TODO:supr
                    ColorRubricAssessment.objects.create(
                        name = self.name + "---" + color.name,
                        color_set_assessment = self,
                        color = color,
                    )
            #TODO
            case "t":
                print("----------------- TODO -----------------")
            case "a":
                print("----------------- TODO -----------------")
        
        self.save()
                                

    def get_nb_max_of_assessment(self) -> int:
        nb_of_assessement = self.nb_of_assessement_max
        match self.type:
            case "r":
                nb_of_assessement = self.color_set.colors.count()
                
            #TODO: Set nb_max_of_assessments
            case "t":
                pass
            case "a":
                pass
        
        print("NB OF assessement MAX CALCULER = ",nb_of_assessement) #TODO:supr
        return nb_of_assessement
    
    @staticmethod
    def get_earliest_from_user(user:User, type_of_assessment, set_of_color:ColorSet = None):
        if set_of_color is None:    
            color_set_assessments = ColorSetAssessment.objects.filter(
                    judge = user, type = type_of_assessment)
        else:
            color_set_assessments = ColorSetAssessment.objects.filter(
                    judge = user, type = type_of_assessment, color_set = set_of_color)
        color_set_assessments.query.add_ordering(DjangoF('date_started').desc())
        return color_set_assessments.first()
    
    
    @staticmethod
    def get_earliest_assessment_from_user(user:User, type_of_assessment):
        assessments = ColorRubricAssessment.objects.filter(
                color_set_assessment = ColorSetAssessment.get_earliest_from_user(
                                                            user,
                                                            type_of_assessment,
                                                            ),
                time_end = None
        )
        assessments.query.add_ordering(DjangoF('time_start').desc(nulls_last=True))
        print("ALL OF THE ASSESSMENTS ARE =",assessments.all()) #TODO:supr
        print("first ASSESSMENT IS =",assessments.first()) #TODO:supr
        return assessments.first()
    
    def is_finished(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END OF SET ASSESSEMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        assessments = ColorRubricAssessment.objects.filter(color_set_assessment=self)
        duration = timedelta(seconds=0)
        for assessement in assessments:
            duration += assessement.duration
        self.assessments_duration = duration
        print("DURATION TOTAL =",duration)

        self.date_ended = now()
        self.save()


class ColorRubricAssessment(models.Model):
    #SetAssessment's name + color's hex code
    name = models.CharField(primary_key=True, max_length=100)
    color_set_assessment = models.ForeignKey(
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
    
 

    
    

