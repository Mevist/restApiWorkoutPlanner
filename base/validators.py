from rest_framework import serializers
from .models import Exercise, User


def validate_exercise_name(value):
    queryset = Exercise.objects.filter(name__iexact=value)
    if queryset.exists():
        raise serializers.ValidationError(f"{value} is already in database")
    return value


def validate_user_name(value):
    queryset = User.objects.filter(name__iexact=value)
    if queryset.exists():
        raise serializers.ValidationError(f"{value} is already in database")
    return value
