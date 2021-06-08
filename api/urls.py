from django.urls import path
from rest_framework.authtoken import views

from .views import (
    UserSignUpView,
    AuthorListCreateView,
    AuthorRetrieveUpdateDestroyView,
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
)


urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
    path('admin/authors/', AuthorListCreateView.as_view(), name='admin-authors'),
    path(
        'admin/authors/<str:id>/',
        AuthorRetrieveUpdateDestroyView.as_view(),
        name='admin-authors-id'
    ),
    path('admin/articles/', ArticleListCreateView.as_view(), name='admin-articles'),
    path(
        'admin/articles/<str:id>/',
        ArticleRetrieveUpdateDestroyView.as_view(),
        name='admin-articles-id'
    ),
]
