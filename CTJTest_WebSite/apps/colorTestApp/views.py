from typing import Any, Dict
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RubricForm
from .models import ColorSetAssessment


# Rubric Views
class RubricTutorialView(LoginRequiredMixin, FormView):
    form_class = RubricForm
    template_name = 'rubric_tutorial.html'
    success_url = reverse_lazy("rubric_test")

    def form_valid(self, form: RubricForm):
        form.show_result()
        return super().form_valid(form)


class RubricTestView(LoginRequiredMixin, FormView):
    template_name = 'rubric_test.html'
    form_class = RubricForm
    success_url = reverse_lazy('thank_you')
    context_object_name = "rubric_test"
    color_to_test = '#262626'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["color_to_test"] = self.color_to_test
        return context

    def form_valid(self, form: RubricForm):
        form.show_result()
        return super().form_valid(form)

