from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RubricForm
from .models import ColorRubricAssessment
from django.utils.timezone import now

# Rubric Views
class RubricTutorialView(LoginRequiredMixin, FormView):
    form_class = RubricForm
    template_name = 'rubric_tutorial.html'
    success_url = reverse_lazy("rubric_assessment")

    def form_valid(self, form: RubricForm):
        form.show_result()
        return super().form_valid(form)


class RubricAssessmentView(LoginRequiredMixin, FormView):
    template_name = 'rubric_assessment.html'
    form_class = RubricForm
    success_url = reverse_lazy('thank_you') #TODO:
    context_object_name = "rubric_assessment"
    color_to_test = '#262626'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["color_to_test"] = self.color_to_test
        return context

    def post(self, request, *args, **kwargs):
        if 'ready' in request.POST and 'start' in request.POST['ready'] :
            print("IL C EST PASSER UN TRUC -----------------------------------------------------------")
            self.begin_Assessment()
        elif 'color_judgement' not in request.POST: 
            return HttpResponseRedirect(redirect_to=reverse_lazy('login'))
        
        return super().post(self, request, *args, **kwargs)
    
    def begin_Assessment(self):
        # if not request.user.is_authenticated: #TODO: Check if the authentification work properly
        #     return self.handle_no_permission()
        print("GROS CACA TOUT POURRIE SES GRAND MORTS")
        # current_datetime = now()

        # ColorRubricAssessment.objects.create(

        #     color = self.color_to_test,
        #     time_start = current_datetime
        # )

    def form_valid(self, form: RubricForm):
        #TODO: check if a date has been set in the last 5 last minutes (this will allow a 5 minutes bug)
        """ There is a bug possible with this function that allow users to skip refreshing the 
        timer if they have already clicked on the 'ready!' button in a 5 minutes interval.
        I don't know a fix to this yet and it's minor """
        color_judgement = form.cleaned_data["color_judgement"]
        form.show_result()
        return super().form_valid(form)

