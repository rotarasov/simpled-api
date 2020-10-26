from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.UserReadUpdateDeleteAPIView.as_view(), name='user-detail'),
    path('', views.UserCreateAPIView.as_view(), name='user-create'),
]
