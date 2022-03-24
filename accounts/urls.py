from django.urls import path
from .views import UserListAPIView

app_name = 'accounts'

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='users')
]