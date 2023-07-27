from django import forms


class RubricForm(forms.Form):

    color_judgement = forms.IntegerField(widget=forms.NumberInput, max_value=255, min_value=0)


class AcjForm(forms.Form):
    choices_of_colors = ( ('A','A'),('B','B') )
    color_comparaison = forms.ChoiceField(widget=forms.RadioSelect, choices=choices_of_colors)


