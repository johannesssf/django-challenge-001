import inspect
from django import test
from django.test import TestCase
from django.test.testcases import SerializeMixin
from rest_framework import serializers

from api.models import Article, Author
from api.serialyzes import ArticleSerializer, AuthorSerializer


class ArticleTest(TestCase):

    def test_article_creation(self):
        author = Author.objects.create(
            name="My Author",
            picture="http://author.pic.com",
        )
        article = Article.objects.create(
            author=author,
            category="Some category",
            title="Article title",
            summary="Article summary",
            first_paragraph="Article first paragraph",
            body="Article body",
        )
        self.assertIsNotNone(article)


class AuthorSerializerTest(TestCase):

    def test_author_serializer_object_to_serializer(self):
        author = Author.objects.create(name="Awesome Author", picture="http://authorpic.com")
        serializer = AuthorSerializer(instance=author)

        self.assertEqual(str(author.id), serializer.data["id"])
        self.assertEqual(author.name, serializer.data["name"])
        self.assertEqual(author.picture, serializer.data["picture"])


class ArticleSerializerTest(TestCase):

    def test_article_serializer_create(self):
        author = Author.objects.create(name="Author 001", picture="http://picture.com")
        article = Article.objects.create(
            author=author,
            category="Category",
            title="Title",
            summary="Summary",
            first_paragraph="First paragraph",
            body="Body",
        )
        serializer = ArticleSerializer(instance=article)

        self.assertEqual(article.author.id, serializer.data["author"])
        self.assertEqual(article.category, serializer.data["category"])
        self.assertEqual(article.title, serializer.data["title"])
        self.assertEqual(article.summary, serializer.data["summary"])
        self.assertEqual(article.first_paragraph, serializer.data["first_paragraph"])
        self.assertEqual(article.body, serializer.data["body"])
