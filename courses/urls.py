from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.CourseReadUpdateDeleteAPIView.as_view(), name='course-detail'),
    path('', views.CourseCreateAPIView.as_view(), name='course-create'),
]
