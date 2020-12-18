from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/messages/', views.MessageListAPIView.as_view(), name='message-list')
]