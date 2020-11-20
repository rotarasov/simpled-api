from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.CourseReadUpdateDeleteAPIView.as_view(), name='course-detail'),
    path('', views.CourseListCreateAPIView.as_view(), name='course-list'),
    path('categories/', views.get_all_categories, name='course-categories'),
    path('languages/', views.get_all_languages, name='course-languages'),
    path('<int:pk>/tasks/', views.TaskListCreateAPIVIew.as_view(), name='task-list'),
    path('<int:course_pk>/tasks/<int:task_pk>/', views.TaskReadUpdateDeleteAPIView.as_view(), name='task-detail'),
    path('<int:course_pk>/tasks/<int:task_pk>/solutions/', views.SolutionListCreateAPIView.as_view(),
         name='solution-list'),
    path('<int:course_pk>/tasks/<int:task_pk>/solutions/<int:solution_pk>/', views.SolutionReadUpdateDeleteAPIVIew.as_view(),
         name='solution-detail'),
]
