from django.urls import path
from . import views

urlpatterns = [
    ###     serializers for exercises resource      ####
    path('exercises/<int:pk>/', views.ExerciseRUDAPIView.as_view()),
    path('exercises/', views.ExerciseListCreateAPIView.as_view()),

    ###     serializers for workoutplans resource   ####
    path('user/<int:id>/workoutplan/',
         views.UserWorkoutPlanListCreateAPIView.as_view()),
    path('user/<int:id>/workoutplan/<int:pk>/',
         views.UserWorkoutPlanRUDAPIView.as_view()),

    ###     serializers for users resource          ####
    path('user/', views.UserListCreateAPIView.as_view()),
    path('user/<int:id>/', views.UserRUDAPIView.as_view()),

    ###     serializers for users resource          ####
    path('user/<int:id>/workoutplan/<int:pk>/history/',
         views.HistoryListCreateAPIView.as_view()),
    path('user/<int:id>/workoutplan/<int:pk>/history/<int:hid>/',
         views.HistoryRUDAPIView.as_view()),
]
