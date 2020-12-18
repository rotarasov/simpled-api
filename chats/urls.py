from django.urls import path

from . import views

urlpatterns = [
    path('chat/<int:pk>/', views.MessageListAPIView.as_view(), name='message-list')
]