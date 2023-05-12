from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Color)
admin.site.register(ColorSet)
admin.site.register(ColorSetAssessment)
admin.site.register(ColorRubricAssessment)
