from typing import Any, Dict
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import IndexForm, RubricTutoForm

class IndexView(LoginRequiredMixin, FormView):
    form_class = IndexForm
    template_name = 'index.html'
    success_url = "thank-you/"

    def form_valid(self, form: IndexForm):
        type_of_test = form.cleaned_data["type_of_test"]
        if(type_of_test == '1'):
            self.success_url = "rubric-tutorial/" 
        return super().form_valid(form)
    

class RubricTutorialView(LoginRequiredMixin, FormView):
    form_class = RubricTutoForm
    template_name = 'rubric_tutorial.html'
    success_url = reverse_lazy("rubric_test")

    def form_valid(self, form: RubricTutoForm):
        form.show_result()
        return super().form_valid(form)


class RubricTestView(LoginRequiredMixin, FormView):
    template_name = 'rubric_test.html'
    form_class = RubricTutoForm
    success_url = reverse_lazy('thank_you')
    context_object_name = "rubric_test"
    color_to_test = '#262626'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["color_to_test"] = self.color_to_test
        return context

    def form_valid(self, form: RubricTutoForm):
        form.show_result()
        return super().form_valid(form)



class ThankYouView(LoginRequiredMixin, TemplateView):
    template_name = 'thank_you.html'



