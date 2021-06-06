from django.urls import path
from rest_framework.authtoken import views

from .views import UserSignUpView, AuthorListCreateView, AuthorRetrieveUpdateDestroyView


urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
    path('admin/authors/', AuthorListCreateView.as_view(), name='admin-authors'),
    path(
        'admin/authors/<str:id>/',
        AuthorRetrieveUpdateDestroyView.as_view(),
        name='admin-authors-id'
    )
]