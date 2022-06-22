from django.views.decorators.http import etag
from rest_framework import generics, status
import datetime

from django.shortcuts import get_object_or_404

from base.models import Exercise, WorkoutPlan, User, History
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .serializers import ExerciseSerializer, ExerciseEmptySerializer, WorkoutPlanSerializer, UserSerializer, \
    HistorySerializer


#### Views for exercises resource ####

class ExerciseCreateAPIView(generics.CreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseEmptySerializer


class ExerciseListCreateAPIView(generics.ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    # def perform_create(self, serializer):
    #     serializer = ExerciseEmptySerializer()
    #     serializer.save()


def get_etag_exercise(request, pk):
    exercise = Exercise.objects.get(pk=pk)
    etag = f'{exercise.name}_{exercise.pk}ver_{exercise.object_version}'.replace(' ', '')
    return etag


class ExerciseRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def perform_update(self, serializer):
        obj = self.get_object()
        instance = serializer.save(object_version=obj.object_version + 1)
        if not instance.description:
            instance.description = "default description"


exercise_rud_apiview = ExerciseRUDAPIView.as_view()
exercise_rud_apiview = etag(etag_func=get_etag_exercise)(exercise_rud_apiview)


#### Views for workoutplans resource ####

class UserWorkoutPlanListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WorkoutPlanSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        print("test1")
        try:
            queryset = User.objects.get(pk=user_id).workoutplans.all()
            return queryset
        except ObjectDoesNotExist:
            queryset = get_object_or_404(User, pk=user_id)
            return queryset

    def perform_create(self, serializer):
        print("test create")
        user_id = self.kwargs['id']
        instance = serializer.save()
        User.objects.get(pk=user_id).workoutplans.add(instance)


def get_etag_workoutplan(request, id, pk):
    user = User.objects.get(pk=id)
    workoutplan = user.workoutplans.get(pk=pk)
    etag = f'{user.name}_{workoutplan.name}_{workoutplan.pk}ver_{workoutplan.object_version}'.replace(' ', '')
    return etag


class UserWorkoutPlanRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

    # def put_parser(self):
    #     exercises_request = self.request.data['exercises']
    #     print(self.request.data)
    #     for exercise_var in exercises_request:
    #         print(exercise_var, exercise_var["pk"], exercise_var["sets"])

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except User.DoesNotExist:
            raise Http404("Given query not found....")

    def perform_update(self, serializer):
        obj = self.get_object()
        instance = serializer.save(object_version=obj.object_version + 1)


user_workoutplan_rud_apiview = UserWorkoutPlanRUDAPIView.as_view()
user_workoutplan_rud_apiview = etag(etag_func=get_etag_workoutplan)(user_workoutplan_rud_apiview)


#### Views for user resource ####

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


def get_etag_user(request, id):
    user = User.objects.get(pk=id)
    etag = f'{user.name}_{user.pk}ver_{user.object_version}'.replace(' ', '')
    return etag


class UserRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except User.DoesNotExist:
            raise Http404("Given query not found....")

    def perform_update(self, serializer):
        obj = self.get_object()
        instance = serializer.save(object_version=obj.object_version + 1)


user_rud_apiview = UserRUDAPIView.as_view()
user_rud_apiview = etag(etag_func=get_etag_user)(user_rud_apiview)


#### Views for user workoutplan history resource ####

class HistoryListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = "hid"
    serializer_class = HistorySerializer

    def post_parser(self):
        user_id = self.kwargs['id']
        workoutplan_pk = self.kwargs['pk']
        workout = {}

        group_users = User.objects.get(pk=user_id).group.all()
        workout_sets = WorkoutPlan.objects.get(pk=workoutplan_pk).sets
        workout_repetitions = WorkoutPlan.objects.get(pk=workoutplan_pk).repetitions
        workout_exercises = WorkoutPlan.objects.get(pk=workoutplan_pk).exercises.all()

        try:
            request_content = self.request.data
            if len(request_content) == 0:
                raise ValueError
        except ValueError:
            for exercise in workout_exercises:
                temp_json = {"repetitions": [0] * workout_sets}
                workout[exercise.name] = temp_json
        else:
            for exercise in workout_exercises:
                temp_json = {}
                if exercise.name in request_content:
                    reps = request_content[exercise.name]["repetitions"]
                    temp_arr = []
                    for rep in reps:
                        temp_arr.append(rep)
                    if len(reps) < workout_sets:
                        diff = workout_sets - len(reps)
                        for _ in range(diff):
                            temp_arr.append(0)
                    temp_json["repetitions"] = temp_arr
                    workout[exercise.name] = temp_json
                else:
                    temp_json["repetitions"] = [0] * workout_sets
                    workout[exercise.name] = temp_json
        return workout

    def get_queryset(self):
        user_id = self.kwargs['id']
        workoutplan_pk = self.kwargs['pk']
        try:
            workoutplan_name = User.objects.get(pk=user_id).workoutplans.get(pk=workoutplan_pk).name
            print(workoutplan_name)
            queryset = History.objects.filter(workoutplan_name__startswith=workoutplan_name)
            return queryset
        except ObjectDoesNotExist:
            queryset = get_object_or_404(History)
            return queryset

    def perform_create(self, serializer):
        user_id = self.kwargs['id']
        workoutplan_pk = self.kwargs['pk']
        workout_name = WorkoutPlan.objects.get(pk=workoutplan_pk).name
        group_users = User.objects.get(id=user_id).group.all()

        temp_name = f'{workout_name}({datetime.date.today()})'
        content = History(workoutplan_name=temp_name, workout=self.post_parser())

        content.save()
        User.objects.get(pk=user_id).history.add(content)
        for user in group_users:
            if not User.objects.get(pk=user.pk).workoutplans.all().filter(name=workout_name).exists():
                User.objects.get(pk=user.pk).workoutplans.add(WorkoutPlan.objects.filter(name=workout_name).first())
            user.history.add(content)


class HistoryRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "hid"
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    # def put_parser(self):
    #     exercises_request = self.request.data['exercises']
    #     print(self.request.data)
    #     for exercise_var in exercises_request:
    #         print(exercise_var, exercise_var["pk"], exercise_var["sets"])

    def perform_destroy(self, instance):
        try:
            super().perform_destroy(instance)
        except User.DoesNotExist:
            raise Http404("Given query not found....")

    def perform_update(self, serializer):
        serializer.save()
