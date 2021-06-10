from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Article, Author


class UserSerialyzer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = super(UserSerialyzer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = "__all__"


class ArticleListLoggedUserSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleListAnonymousUserSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ("id", "author", "category", "title", "summary", "first_paragraph")


class ArticleListSearchSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ("id", "author", "category", "title", "summary")
