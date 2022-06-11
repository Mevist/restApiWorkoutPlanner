from rest_framework import generics, status
import datetime

from django.shortcuts import get_object_or_404

from base.models import Exercise, WorkoutPlan, User, History
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .serializers import ExerciseSerializer, WorkoutPlanSerializer, UserSerializer, HistorySerializer


#### Views for exercises resource ####

class ExerciseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        serializer.save()


class ExerciseRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.description:
            instance.description = "default description"


#### Views for workoutplans resource ####

class UserWorkoutPlanListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WorkoutPlanSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        try:
            queryset = User.objects.get(pk=user_id).workoutplans.all()
            return queryset
        except ObjectDoesNotExist:
            queryset = get_object_or_404(User, pk=user_id)
            return queryset

    def perform_create(self, serializer):
        user_id = self.kwargs['id']
        instance = serializer.save()
        User.objects.get(pk=user_id).workoutplans.add(instance)


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
        serializer.save()



    ### method for future improvments ####
    # def perform_update(self, serializer):
    #     user_id = self.kwargs['id']
    #     workoutplan_pk = self.kwargs['pk']
    #     instance = serializer.save()
    #     workoutplan_obj = User.objects.get(pk=user_id).workoutplans.get(pk=workoutplan_pk)
    #     print(workoutplan_obj.sets)



#### Views for user resource ####

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


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
        instance = serializer.save()
        if not instance.email:
            instance.type = "-----"

#### Views for user workoutplan history resource ####

class HistoryListCreateAPIView(generics.ListCreateAPIView):
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
            queryset = History.objects.filter(workoutplan_name__startswith = workoutplan_name)
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
        content = History(workoutplan_name=temp_name,workout=self.post_parser())
        # content["name"] = temp_name
        # content["workout"] = self.post_parser()

        content.save()
        User.objects.get(pk=user_id).add(content)
        for user in group_users:
           user.history.add(content)

class HistoryRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "hid"
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
        serializer.save()


