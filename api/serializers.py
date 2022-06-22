from rest_framework import serializers
from base.models import Exercise, WorkoutPlan, User, History
from rest_framework.reverse import reverse

from base.validators import validate_exercise_name, validate_user_name


class ExerciseEmptySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Exercise
        fields = ['url']

    def create(self, validated_data):
        return super().create(validated_data)

    def get_url(self, obj):
        latest_id = Exercise.objects.latest('id').id
        print(latest_id)
        url_temp = f'{reverse("exercise-list")}/{latest_id}/'
        return url_temp
        # request = self.context.get('request ')
        # obj_temp = Exercise.objects.latest('id')
        # if request is None:
        #     return None
        # # return reverse("exercise-list", kwargs={"id": self.id}, request=request)

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
    # id = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = '__all__'

        # fields = [
        #     'pk'
        #     'name',
        #     'email',
        #     'password',
        #     'workoutplans',
        #     'group'
        # ]

    # def save(self):
    #     name = self.validated_data("name")
    #     email = self.validated_data("email")
    #     password = self.validated_data("password")
    #     workoutplans = self.validated_data("workoutplans")
    #     group = self.validated_data("group")
    #     history = self.validated_data("history")
    #     object_version = self.validated_data("object_version")


    # def get_id(self,obj):
    #     return obj.get_id()


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'
        # fields = [
        #     'hid',
        #     'date',
        #     'workout',
        #     'modified'
        # ]