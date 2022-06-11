from django.contrib import admin

# Register your models here.
from .models import Exercise, WorkoutPlan, User


admin.site.register(Exercise)
admin.site.register(WorkoutPlan)
admin.site.register(User)