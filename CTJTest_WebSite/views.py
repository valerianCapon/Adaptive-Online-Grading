from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import IndexForm

class IndexView(LoginRequiredMixin, FormView):
    form_class = IndexForm
    template_name = 'index.html'
    success_url = "thank-you/"

    def form_valid(self, form: IndexForm):
        type_of_test = form.cleaned_data["type_of_test"]
        if(type_of_test == '1'):
            self.success_url = "rubric-tutorial/" 
        return super().form_valid(form)


class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'thank_you.html'



