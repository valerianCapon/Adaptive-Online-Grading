from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from .apps.colorTestApp.models import ColorSet, ColorSetAssessment
from .forms import IndexForm

class IndexView(LoginRequiredMixin, FormView):
    form_class = IndexForm
    template_name = 'index.html'
    success_url = "thank-you/"

    def form_valid(self, form: IndexForm):
        type_of_test = form.cleaned_data["type_of_test"]
        name_of_color_set_selected = form.cleaned_data["color_set"]
 
        current_color_set = ColorSet.objects.get(name=name_of_color_set_selected)
        #We get a proper User instead of request.user which is an AbstractBaseUser
        current_user = User.objects.get(username=self.request.user.username)  
        current_datetime = now()

        earliest_set_assessment = ColorSetAssessment.get_earliest_from_user(current_user, type_of_test, current_color_set)
        if earliest_set_assessment is None or earliest_set_assessment.date_ended is not None:
            print("CREATING A NEW COLOR SET ASSESSMSENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!") #TODO:suppr
            new_set_assessment = ColorSetAssessment.objects.create(
                name = current_user.username + "---" + type_of_test + "---" + name_of_color_set_selected + "---" + str(current_datetime),
                type = type_of_test,
                color_set = current_color_set,
                judge = current_user,
                date_started = current_datetime,
            )
            new_set_assessment.nb_of_assessement_max = new_set_assessment.get_nb_max_of_assessment()
            new_set_assessment.save
            new_set_assessment.create_assessments()
        print("OH ON EST PASSER PAR LA et le easliest set assessment est :",earliest_set_assessment)

        #TODO: SI A DEJA ETAIT CREE ALORS SKIP TUTORIAL
        if(type_of_test == 'r'):
            self.success_url = "rubric-tutorial/"
        elif(type_of_test == 'a'):
            self.success_url = "acj-tutorial/"
        # elif(type_of_test == 't'):
        #     self.success_url = "tcj-tutorial/"

        return super().form_valid(form)


class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'thank_you.html'



