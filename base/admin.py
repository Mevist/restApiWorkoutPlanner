from django.contrib import admin

# Register your models here.
from .models import Exercise, WorkoutPlan, User,History


admin.site.register(Exercise)
admin.site.register(WorkoutPlan)
admin.site.register(User)
admin.site.register(History)