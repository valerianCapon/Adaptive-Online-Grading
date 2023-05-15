from django import forms
from .apps.colorTestApp.models import ColorSet

class IndexForm(forms.Form):
    choices_of_set = [(color_set.name, color_set.name) for _, color_set in enumerate(ColorSet.objects.all())]
    choices_of_test = (('r','Rubric Test'),('t','CTJ Test'),('a','ACJ Test'))

    color_set = forms.ChoiceField(widget=forms.Select, choices=choices_of_set)
    type_of_test = forms.ChoiceField(widget=forms.RadioSelect, choices=choices_of_test)



