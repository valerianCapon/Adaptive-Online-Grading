from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .apps.colorTestApp.models import ColorSet, ColorSetAssessment
from datetime import datetime
from .forms import IndexForm

class IndexView(LoginRequiredMixin, FormView):
    form_class = IndexForm
    template_name = 'index.html'
    success_url = "thank-you/"

    def form_valid(self, form: IndexForm):
        type_of_test = form.cleaned_data["type_of_test"]
        # color_set_selected = form.cleaned_data["color_set"]

        # current_user = self.request.user

        # color_set_assessement = ColorSetAssessment.objects.create(
        #     name = current_user.username + type_of_test,
        #     type = type_of_test,
        #     judge = self.request.user,
        #     nb_of_assmnt_max = 5, #TODO: define a nb max
        # )
        # color_set_assessement.name += color_set_assessement.date_started

        # color_set_assessement.save()

        if(type_of_test == 'r'):
            self.success_url = "rubric-tutorial/" 
        return super().form_valid(form)


class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'thank_you.html'



