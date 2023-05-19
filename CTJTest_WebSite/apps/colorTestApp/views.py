from typing import Any, Dict
from django import http
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RubricForm
from .models import ColorRubricAssessment, ColorSetAssessment
from django.utils.timezone import now
from datetime import timedelta

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
    success_url = reverse_lazy('thank_you') #TODO:sûre ? 
    context_object_name = "rubric_assessment"
    color_rubric_assessment = None  #Is set within override of setup()
    type_of_assessment = 'r'
     
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.color_rubric_assessment = ColorSetAssessment.get_last_assessment_from_user(
                                            self.request.user, self.type_of_assessment )


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        current_user = self.request.user
        current_color_set_assessment = ColorSetAssessment.get_last_from_user(current_user, self.type_of_assessment)

        
        print("CURRENT COLOR SET ASSMNT = ", current_color_set_assessment.all()) #TODO:supr
        current_color_set_assessment = current_color_set_assessment.latest('date_started')

        self.color_rubric_assessment = ColorRubricAssessment.objects.filter(
            color_set_assessment= current_color_set_assessment,
            time_end = None,
        )
        print("COLOR RUBRIC ASSMNTS = ", self.color_rubric_assessment.all()) #TODO:supr
        self.color_rubric_assessment = self.color_rubric_assessment.latest('time_start')


        print("AFFICHE CE GARS = ",self.color_rubric_assessment) #TODO:supr
        context["color_to_test"] = self.color_rubric_assessment.color
        return context

    def post(self, request, *args, **kwargs):
        if 'ready' in request.POST and 'start' in request.POST['ready'] :
            print(" -------------------------- START ---------------------------------")
            self.begin_Assessment()
        elif 'color_judgement' not in request.POST: 
            return HttpResponseRedirect(redirect_to=reverse_lazy('login'))
        
        return super().post(self, request, *args, **kwargs)
    
    def begin_Assessment(self):
        # if not request.user.is_authenticated: #TODO: Check if the authentification work properly
        #     return self.handle_no_permission()
        print("GROS CACA TOUT POURRIE SES GRAND MORTS")
        self.color_rubric_assessment.time_start = now()
        self.color_rubric_assessment.save()
        

    def form_valid(self, form: RubricForm):
        """ There is a bug possible with this function that allow users to skip refreshing the 
        start timer if they have already clicked on the 'ready!' button in a 5 minutes interval.
        I don't know a fix to this yet and it's minor """
        
        #Get the dates to make sure the form has been correctly sent
        started_at = self.color_rubric_assessment.time_start
        ended_at = now()

        #TODO: Check if it's working
        print("check bool = ",started_at == None or started_at < ended_at - timedelta(minutes=5) )
        if started_at == None or started_at < ended_at - timedelta(minutes=5) :
           return HttpResponseRedirect(redirect_to='rubric_assessment') 
        
        color_judgement = form.cleaned_data["color_judgement"]
        lasted_for = (ended_at - started_at)

        self.color_rubric_assessment.time_end = ended_at
        self.color_rubric_assessment.duration = lasted_for
        self.color_rubric_assessment.shade_guessed = color_judgement


        self.color_rubric_assessment.save()
        form.show_result()
        return super().form_valid(form)

