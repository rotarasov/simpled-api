from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.CourseReadUpdateDeleteAPIView.as_view(), name='course-detail'),
    path('', views.CourseCreateAPIView.as_view(), name='course-create'),
    path('categories/', views.get_all_categories, name='course-categories'),
    path('languages/', views.get_all_languages, name='course-languages')
]
