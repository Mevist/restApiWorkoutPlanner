from rest_framework import serializers
from base.models import Exercise, WorkoutPlan, User, History

from rest_framework.reverse import reverse
from base.validators import validate_exercise_name, validate_user_name


class ExerciseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_exercise_name])

    class Meta:
        model = Exercise
        fields = '__all__'


class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(read_only=True, many=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'pk',
            'name',
            'type',
            'exercises',
            'sets',
            'repetitions'
        ]


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_user_name])

    class Meta:
        model = User
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'