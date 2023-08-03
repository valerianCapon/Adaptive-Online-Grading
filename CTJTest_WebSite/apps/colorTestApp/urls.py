from django.urls import path

from . import views

urlpatterns = [

    #Rubric
    path('rubric-tutorial/', views.RubricTutorialView.as_view(), name="rubric_tutorial"),
    path('rubric-assessment/', views.RubricAssessmentView.as_view(), name="rubric_assessment"),
    #ACJ
    path('acj-tutorial/', views.AcjTutorialView.as_view(), name="acj_tutorial"),
    path('acj-assessment/', views.AcjAssessmentView.as_view(), name="acj_assessment"),
    #CTJ
]
