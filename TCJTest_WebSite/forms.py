from django import forms


class IndexForm(forms.Form):
    choices_of_set = (('1','Set number 1'),('2','Set number 2'),('3','Set number 3'))
    choices_of_test = (('1','Rubric Test'),('2','TCJ Test'),('3','ACJ Test'))

    set_of_color = forms.ChoiceField(widget=forms.Select, choices=choices_of_set)
    type_of_test = forms.ChoiceField(widget=forms.RadioSelect, choices=choices_of_test)


class RubricTutoForm(forms.Form):
    color_judgement = forms.IntegerField(widget=forms.NumberInput, max_value=255, min_value=0)

    def show_result(self):
        print("RESULTAT FORMULAIRE =",self.cleaned_data["color_judgement"])