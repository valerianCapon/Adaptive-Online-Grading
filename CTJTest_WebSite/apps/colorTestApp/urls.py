from django.urls import path

from . import views

urlpatterns = [

    #Rubric
    path('rubric-tutorial/', views.RubricTutorialView.as_view(), name="rubric_tutorial"),
    path('rubric-test/', views.RubricTestView.as_view(), name="rubric_test"),

    #ACJ

    #CTJ
]
