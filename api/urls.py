from django.urls import path
from rest_framework.authtoken import views

from .views import UserSignUpView


urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
]