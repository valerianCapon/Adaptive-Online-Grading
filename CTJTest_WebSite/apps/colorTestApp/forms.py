from django import forms
from .models import ColorRubricAssessment, ColorSetAssessment

class RubricForm(forms.Form):

    color_judgement = forms.IntegerField(widget=forms.NumberInput, max_value=255, min_value=0)

    def show_result(self):
        print("RESULTAT FORMULAIRE =",self.cleaned_data["color_judgement"])

