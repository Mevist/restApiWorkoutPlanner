from django.urls import path
from . import views

urlpatterns = [
    ###     serializers for exercises resource      ####
    path('exercises/<int:pk>/', views.exercise_rud_apiview),
    path('exercises/', views.ExerciseListCreateAPIView.as_view()),
    path('exercises', views.ExerciseCreateAPIView.as_view(), name='exercise-list'),

    ###     serializers for workoutplans resource   ####
    path('user/<int:id>/workoutplan/',
         views.UserWorkoutPlanListCreateAPIView.as_view()),
    path('user/<int:id>/workoutplan/<int:pk>/',
         views.user_workoutplan_rud_apiview),

    ###     serializers for users resource          ####
    path('user/', views.UserListCreateAPIView.as_view()),
    path('user/<int:id>/', views.user_rud_apiview),

    ###     serializers for users resource          ####
    path('user/<int:id>/workoutplan/<int:pk>/history/',
         views.HistoryListCreateAPIView.as_view()),
    path('user/<int:id>/workoutplan/<int:pk>/history/<int:hid>/',
         views.HistoryRUDAPIView.as_view()),
]
