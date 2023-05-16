from django import forms

class RubricForm(forms.Form):
    color_judgement = forms.IntegerField(widget=forms.NumberInput, max_value=255, min_value=0)

    def show_result(self):
        print("RESULTAT FORMULAIRE =",self.cleaned_data["color_judgement"])



class ReadyForm(forms.Form):
    ready = forms.CharField(widget=forms.HiddenInput, max_length=5, min_length=5, initial="ready")
