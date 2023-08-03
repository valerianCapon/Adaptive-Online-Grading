from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from colorfield.fields import ColorField
from collections import namedtuple
from django.db.models import F as DjangoF
from django.utils.timezone import now
from datetime import timedelta

from .algorithms import ACJ


class Color(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    color_code = ColorField(unique=True) # exemple : white is #FFFFFF

    def __str__(self) -> str:
        return self.name

    """
    Return the RGB values of the hex color as a named tuple
    Example: rgb_tuple = color1.rgb_values()
            red = rgb_tuple.red
    """
    def get_average_rgb(self) -> int:
        rgb = self.get_rgb_values()
        result = rgb.red
        result += rgb.blue
        result += rgb.green
        return  int(result / 3) 
        
    
    def get_rgb_values(self) -> tuple:
        #index start at 1 because color_code[0] is # 
        red = int(self.color_code[1:3], 16)
        blue = int(self.color_code[3:5], 16)
        green = int(self.color_code[5:7], 16)
        return namedtuple("RGB", ["red", "blue", "green"])(red=red, blue=blue, green=green)


class ColorSet(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    description = models.TextField(max_length=200, blank=True)
    colors = models.ManyToManyField(Color, blank=True, related_name='color_sets')

    def __str__(self) -> str:
        return self.name


class ColorSetAssessment(models.Model):
    """ name = judge --- type --- color set's name --- date """
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
    
    """    
    Generate the assessment of the set of the Color Set's assessment.
    It only have to be called one time for the Rubric assessments
    But need to be called one at a time for the ACJ and CTJ assessments
    return the algorithms' parameter (in the rubric case it will just return None)
    """ 
    def create_assessments(self):
        result = None
        list_of_colors = self.color_set.colors.all()
        print(list_of_colors) #TODO:supr

        match self.type:
            #Rubric type of assessments
            case "r":
                for set_nb, color in zip(range(1,self.nb_of_assessement_max+1), list_of_colors):
                    print("creation of assesment nb =", set_nb," and color =",color.name) #TODO:supr
                    ColorRubricAssessment.objects.create(
                        name = self.name + "---" + color.name,
                        color_set_assessment = self,
                        color = color,
                    )

            #Acj type of assessments
            case "a":
                #Get all the colors and put them in this format : [("color's name", color_value) ... ]
                colors = []
                for color in list_of_colors :
                    colors.append((color.name, color.get_average_rgb()))
                print("colors are =",colors)#TODO:supr
                
                #Get all the Assessments made to make a list of all of the comparisons done
                #in this format : [ (color winner's name, color looser's name) ...]
                acj_assessments_objects = ColorAcjAssessment.objects.filter(
                    color_set_assessment=self
                    ).exclude(color_selected__isnull=True)
                
                acj_comparisons = []
                for acj_assessment in acj_assessments_objects:
                    if acj_assessment.color_A == acj_assessment.color_selected:
                        new_comparison = (acj_assessment.color_A.name, acj_assessment.color_B.name)
                    else:
                        new_comparison = (acj_assessment.color_B.name, acj_assessment.color_A.name)

                    acj_comparisons.append(new_comparison)
                

                print("acj_comparisons =",acj_comparisons)#TODO:supr

                result = ACJ.acj_iteration(colors,acj_comparisons)
                print("RESULT OF ACJ =",result)#TODO:supr
                
                if not result["finished"] and len(acj_comparisons) < self.nb_of_assessement_max-1:
                    print("color A name = ",result["new_comparison"][0])
                    print("color A name = ",result["new_comparison"][1])
                    color_A = Color.objects.get(name=result["new_comparison"][0])
                    color_B = Color.objects.get(name=result["new_comparison"][1])

                    print(ColorAcjAssessment.objects.create(
                            name = self.name + "---" + color_A.name + "---" + color_B.name + "---" + str(self.nb_of_assessement),
                            color_set_assessment = self,
                            color_A = color_A,
                            color_B = color_B,
                    ))#TODO:modify
                
            case "t":
                print("----------------- TODO -----------------")

        
        self.save()
        return result


    def get_nb_max_of_assessment(self) -> int:
        nb_of_assessement = self.nb_of_assessement_max
        match self.type:
            case "r":
                nb_of_assessement = self.color_set.colors.count()                
            case "a":
                #20 is totaly arbitrary and can probably be computed from the number of colors
                # and the complexity of the acj algorithme
                nb_of_assessement = 20

            case "t":
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
        match type_of_assessment:
            case "r":
                assessments = ColorRubricAssessment.objects.filter(
                        color_set_assessment = ColorSetAssessment.get_earliest_from_user(
                                                                    user,
                                                                    type_of_assessment,
                                                                    ),
                        time_end = None
                )
                assessments.query.add_ordering(DjangoF('time_start').desc(nulls_last=True))
            case "a":
                assessments = ColorAcjAssessment.objects.filter(
                        color_set_assessment = ColorSetAssessment.get_earliest_from_user(
                                                                    user,
                                                                    type_of_assessment,
                                                                    ),
                        time_end = None
                )
                assessments.query.add_ordering(DjangoF('time_start').desc(nulls_last=True))
        #TODO:CTJ
        print("ALL OF THE ASSESSMENTS ARE =",assessments.all()) #TODO:supr
        print("first ASSESSMENT IS =",assessments.first()) #TODO:supr
        return assessments.first()
    
    def is_finished(self):
        #TODO:CTJ
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END OF SET ASSESSEMENT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        match self.type:
            case 'r':
                assessments = ColorRubricAssessment.objects.filter(color_set_assessment=self)
            case 'a':
                assessments = ColorAcjAssessment.objects.filter(color_set_assessment=self)

        duration = timedelta(seconds=0)
        for assessement in assessments:
            duration += assessement.duration
        self.assessments_duration = duration
        print("DURATION TOTAL =",duration)

        self.date_ended = now()
        self.save()


class ColorRubricAssessment(models.Model):
    #SetAssessment's name + "---" + color's name   
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
    
 

class ColorAcjAssessment(models.Model):
    #SetAssessment's name + "---" + color A's name + "---" + color B's name + "---" + nb of assessment already made
    name = models.CharField(primary_key=True, max_length=100)
    color_set_assessment = models.ForeignKey(
        ColorSetAssessment,
        on_delete=models.CASCADE,
        related_name="acj_assessments",
    )
    color_A = models.ForeignKey(
        Color, on_delete=models.PROTECT, related_name="color_a_of_acj_assessment"
    )
    color_B = models.ForeignKey(
        Color, on_delete=models.PROTECT, related_name="color_b_of_acj_assessment"
    )

    color_selected = models.ForeignKey(
        Color, blank=True, null=True, on_delete=models.PROTECT, related_name="acj_assessments"
    )

    """
    Store all of the important data related to the algorithme
    {
        SSR : float or None,  #Scale Separation Reliability
        estimated_values : [ (color's name, color's estimated value), ...],
        comparisons: [(winning color's name, loosing color's name)...],
    }
    """
    acj_data = models.JSONField(blank=True, null=True)

    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Color Acj Assessment"
        get_latest_by = "time_start"

    def __str__(self) -> str:
        return self.name

    def get_judge(self):
        return self.color_set_assmt.judge
    

