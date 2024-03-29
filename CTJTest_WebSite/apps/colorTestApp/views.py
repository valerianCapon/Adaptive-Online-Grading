from django.http import HttpRequest, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.timezone import now

from .forms import RubricForm, AcjForm
from .models import ColorSetAssessment

from datetime import timedelta
from typing import Any, Dict



#------------------------------------- Rubric -------------------------------------
class RubricTutorialView(LoginRequiredMixin, FormView):
    form_class = RubricForm
    template_name = 'rubric_tutorial.html'
    success_url = reverse_lazy("rubric_assessment")


class RubricAssessmentView(LoginRequiredMixin, FormView):
    template_name = 'rubric_assessment.html'
    form_class = RubricForm
    success_url = reverse_lazy('rubric_assessment') #TODO:sûre ? 
    context_object_name = "rubric_assessment"
    color_rubric_assessment = None  #Is set in the override of setup()
    type_of_assessment = 'r'
     
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        current_user = User.objects.get(username=self.request.user.username)  
        self.color_rubric_assessment = ColorSetAssessment.get_earliest_assessment_from_user(current_user, self.type_of_assessment)
        print("========================================\nSETUP rubric assment to do =", self.color_rubric_assessment.name)


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        

        current_user = self.request.user
        current_color_set_assessment = ColorSetAssessment.get_earliest_from_user(current_user, self.type_of_assessment)

        print("----------------------------------- NEW CONTEXT ----------------------------------------") #TODO:supr
        print("CURRENT COLOR SET assessement = ", current_color_set_assessment) #TODO:supr
        print(" judge =", current_color_set_assessment.judge, 
              "\n color set =", current_color_set_assessment.color_set,
              "\n color date started =", current_color_set_assessment.date_started, 
              "\n color date ended =", current_color_set_assessment.date_ended,
              "\n color type =", current_color_set_assessment.type, ) #TODO:supr

        context["color_to_test"] = self.color_rubric_assessment.color.color_code
        return context

    def post(self, request, *args, **kwargs):
        if 'ready' in request.POST and 'start' in request.POST['ready'] :
            print(" -------------------------- START ---------------------------------") #TODO:supr
            # if not request.user.is_authenticated: #TODO: Check if the authentification work properly
            #     return self.handle_no_permission()
            self.color_rubric_assessment.time_start = now()
            self.color_rubric_assessment.save()
            print("ON START A = ", self.color_rubric_assessment.time_start) #TODO:supr
        elif 'color_judgement' not in request.POST: 
            return HttpResponseRedirect(redirect_to=reverse_lazy('login'))
        
        return super().post(self, request, *args, **kwargs)
    


    def form_valid(self, form: RubricForm):
        """ There is a bug possible with this function that allow users to skip refreshing the 
        start timer if they have already clicked on the 'ready!' button in a 1minute 30s interval.
        I don't know a fix to this yet and it's minor """
        
        #Get the dates to make sure the form has been correctly sent
        started_at = self.color_rubric_assessment.time_start
        ended_at = now()
        print("ça a bien start ? = ", started_at) #TODO:supr
        if started_at == None or timedelta(minutes=1,seconds=30) <= (ended_at - started_at)  :
            print("FORM WIHOUT START BUUUUUUUUUUUUUUUUUUUUUUUUUUUUGGGGGGGGGGGGGG") #TODO:supr
            print("cauz no start ?",started_at == None) #TODO:supr

            if started_at is not None: #TODO:supr
                print("cauz wtf 1 minutes 30", timedelta(minutes=1,seconds=30) <= (ended_at - started_at) ) #TODO:supr
                print("delta time diff = ", (ended_at - started_at) ) #TODO:supr
            return HttpResponseRedirect(redirect_to=reverse_lazy('index')) 
        
        color_judgement = form.cleaned_data["color_judgement"]
        lasted_for = (ended_at - started_at)

        self.color_rubric_assessment.time_end = ended_at
        self.color_rubric_assessment.duration = lasted_for
        self.color_rubric_assessment.shade_guessed = color_judgement

        self.color_rubric_assessment.color_set_assessment.nb_of_assessement += 1
        self.color_rubric_assessment.color_set_assessment.save()
        self.color_rubric_assessment.save()

    
        nb_of_assessement_done = self.color_rubric_assessment.color_set_assessment.nb_of_assessement
        nb_of_assessement_max = self.color_rubric_assessment.color_set_assessment.nb_of_assessement_max
        print("done =", nb_of_assessement_done, "| total =",nb_of_assessement_max) #TODO:supr
        if nb_of_assessement_done == nb_of_assessement_max:
            self.color_rubric_assessment.color_set_assessment.is_finished()

            print("DONE FINITO") #TODO:supr
            self.success_url = reverse_lazy('thank_you')
         
         
        print("SECCESSSSSSSS =", self.success_url) #TODO:supr
        return super().form_valid(form)


#------------------------------------- ACJ -------------------------------------
class AcjTutorialView(LoginRequiredMixin, FormView):
    form_class = AcjForm
    template_name = 'acj_tutorial.html'
    success_url = reverse_lazy('acj_assessment')

    def form_valid(self, form: AcjForm):
        return super().form_valid(form)



class AcjAssessmentView(LoginRequiredMixin, FormView):
    template_name = 'acj_assessment.html'
    form_class = AcjForm
    success_url = reverse_lazy('acj_assessment') 
    context_object_name = "acj_assessment"
    colors_acj_assessment = None  #Is set in the override of setup()
    type_of_assessment = 'a'


    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        current_user = User.objects.get(username=self.request.user.username)  
        self.color_acj_assessment = ColorSetAssessment.get_earliest_assessment_from_user(current_user, self.type_of_assessment)
        print("========================================\nSETUP acj assessment to do =", self.color_acj_assessment.name)


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        

        current_user = self.request.user
        current_color_set_assessment = ColorSetAssessment.get_earliest_from_user(current_user, self.type_of_assessment)

        print("----------------------------------- NEW CONTEXT ----------------------------------------") #TODO:supr
        print("CURRENT COLOR SET assessement = ", current_color_set_assessment) #TODO:supr
        print(" judge =", current_color_set_assessment.judge, 
              "\n color set =", current_color_set_assessment.color_set,
              "\n color date started =", current_color_set_assessment.date_started, 
              "\n color date ended =", current_color_set_assessment.date_ended,
              "\n color type =", current_color_set_assessment.type, )

        #TODO: color code
        context["color_A"] = self.color_acj_assessment.color_A.color_code
        context["color_B"] = self.color_acj_assessment.color_B.color_code

        return context    

    def post(self, request, *args, **kwargs):
        if 'ready' in request.POST and 'start' in request.POST['ready'] :
            print(" -------------------------- START ---------------------------------") #TODO:supr
            # if not request.user.is_authenticated: #TODO: Check if the authentification work properly
            # self.handle_no_permission()
            self.color_acj_assessment.time_start = now()
            self.color_acj_assessment.save()
            print("ON START A = ", self.color_acj_assessment.time_start) #TODO:supr
        #Check the validity of the post
        elif 'color_comparaison' not in request.POST: 
            return HttpResponseRedirect(redirect_to=reverse_lazy('login'))
        
        print("LA REQUETE EST :",request.body)
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form: AcjForm):
        print("OOOOOOOOOOOOOOOOO Y A UN FORMULAIRE LAAAAAAAAAAAAAAAAAAAA")
        """ There is a bug possible with this function that allow users to skip refreshing the 
        start timer if they have already clicked on the 'ready!' button in a 1minute 30s interval.
        I don't know a fix to this yet and it's minor """
        
        #Get the dates to make sure the form has been correctly sent
        started_at = self.color_acj_assessment.time_start
        ended_at = now()
        print("ça a bien start ? = ", started_at) #TODO:supr

        if started_at == None or timedelta(minutes=5) <= (ended_at - started_at)  :
            print("FORM WIHOUT START BUUUUUUUUUUUUUUUUUUUUUUUUUUUUGGGGGGGGGGGGGG") #TODO:supr
            print("cauz no start ?",started_at == None) #TODO:supr

            if started_at is not None: #TODO:supr
                print("cauz wtf 1 minutes 30", timedelta(minutes=1,seconds=30) <= (ended_at - started_at) ) #TODO:supr
                print("delta time diff = ", (ended_at - started_at) ) #TODO:supr
            return HttpResponseRedirect(redirect_to=reverse_lazy('index')) 
        
        color_comparaison = form.cleaned_data["color_comparaison"]
        print("LA COULEUR SELECTIONNER EST :",color_comparaison)
        lasted_for = (ended_at - started_at)

        self.color_acj_assessment.time_end = ended_at
        self.color_acj_assessment.duration = lasted_for
        if color_comparaison == "A":
            self.color_acj_assessment.color_selected = self.color_acj_assessment.color_A
        else:
            self.color_acj_assessment.color_selected = self.color_acj_assessment.color_B

        self.color_acj_assessment.color_set_assessment.nb_of_assessement += 1
        
        #We generate the next assessment to do 
        #and we store in the database parameters from the acj algorithm 
        result = self.color_acj_assessment.color_set_assessment.create_assessments()
        self.color_acj_assessment.acj_data = result

        self.color_acj_assessment.color_set_assessment.save()
        self.color_acj_assessment.save()

        #Checking if it was the last assessment to do
        nb_of_assessement_done = self.color_acj_assessment.color_set_assessment.nb_of_assessement
        nb_of_assessement_max = self.color_acj_assessment.color_set_assessment.nb_of_assessement_max
        print("done =", nb_of_assessement_done, "| total =",nb_of_assessement_max) #TODO:supr

        if result["finished"] or nb_of_assessement_done == nb_of_assessement_max:
            self.color_acj_assessment.color_set_assessment.is_finished()
            print("DONE FINITO") #TODO:supr
            self.success_url = reverse_lazy('thank_you')
         
         
        print("SECCESSSSSSSS =", self.success_url) #TODO:supr
        return super().form_valid(form)


