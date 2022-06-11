import datetime

from django.db import models


# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    # sets = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
    # repetitions = models.DecimalField(max_digits=2, decimal_places=0,null=True, blank=True)
    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    name = models.CharField(max_length=50)
    TYPE = (
        ('Power', 'Power'),
        ('Speed', 'Speed'),
        ('Flexibility', 'Flexibility')
    )
    exercises = models.ManyToManyField(Exercise)
    type = models.CharField(max_length=100, null=True, blank=True, choices=TYPE)
    sets = models.JSONField(blank=True)
    repetitions = models.JSONField(blank=True)

    # sets = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class History(models.Model):
    workoutplan_name = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    workout = models.JSONField(blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        temp = f'{self.name}({self.pk}-{self.date})'
        return temp

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=100, blank=True)
    workoutplans = models.ManyToManyField(WorkoutPlan, blank=True)
    group = models.ManyToManyField("self", blank=True)
    history = models.ManyToManyField(History, blank=True)

    def __str__(self):
        return self.name



