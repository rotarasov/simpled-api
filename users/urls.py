from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('<int:pk>', views.UserReadUpdateDeleteAPIView.as_view(), name='user-detail'),
    path('', views.UserCreateAPIView.as_view(), name='user-create'),
    path('token/', views.CustomTokenObtainPairAPIView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('<int:pk>/change-password/', views.update_user_password, name='change-password')
]
