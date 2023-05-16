from django.urls import path

from . import views

urlpatterns = [

    #Rubric
    path('rubric-tutorial/', views.RubricTutorialView.as_view(), name="rubric_tutorial"),
    path('rubric-assessment/', views.RubricAssessmentView.as_view(), name="rubric_assessment"),
    #ACJ

    #CTJ
]
