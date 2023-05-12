from django import forms
from .apps.colorTestApp.models import ColorSet

class IndexForm(forms.Form):
    choices_of_set = [(i+1, color_set.name) for i, color_set in enumerate(ColorSet.objects.all())]
    print(choices_of_set)
    choices_of_test = (('r','Rubric Test'),('t','CTJ Test'),('a','ACJ Test'))

    color_set = forms.ChoiceField(widget=forms.Select, choices=choices_of_set)
    type_of_test = forms.ChoiceField(widget=forms.RadioSelect, choices=choices_of_test)



