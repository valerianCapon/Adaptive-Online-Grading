from typing import Any
from django.http import HttpRequest, HttpResponse
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
        current_user = self.request.user
        current_datetime = now()

        ColorSetAssessment.objects.create(
            name = current_user.username + "_" + type_of_test + "_" + str(current_datetime),
            type = type_of_test,
            color_set = current_color_set,
            judge = self.request.user,
            date_started = current_datetime,
        ).create_assmnts()

        if(type_of_test == 'r'):
            self.success_url = "rubric-tutorial/" 
        return super().form_valid(form)


class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'thank_you.html'



