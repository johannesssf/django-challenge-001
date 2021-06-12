from django.contrib.auth.models import User, AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Author, Article
from .serialyzes import (
    UserSerialyzer,
    AuthorSerializer,
    ArticleSerializer,
    ArticleListSearchSerializer,
    ArticleListLoggedUserSerializer,
    ArticleListAnonymousUserSerializer,
)


class UserSignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialyzer
    lookup_field = "username"


class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AuthorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = "id"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ArticleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "id"
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ArticleListSearchView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']


class ArticleListView(RetrieveAPIView):
    queryset = Article.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if isinstance(self.request.user, AnonymousUser):
            return ArticleListAnonymousUserSerializer
        return ArticleListLoggedUserSerializer
