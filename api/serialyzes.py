from api.models import Author
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
        fields = ("id", "name", "picture")


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "author", "category", "title", "summary", "first_paragraph", "body")
