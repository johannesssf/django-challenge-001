from django.test import TestCase

from api.models import Article, Author
from api.serialyzes import (
    ArticleSerializer,
    AuthorSerializer,
    ArticleListLoggedUserSerializer,
    ArticleListAnonymousUserSerializer,
    ArticleListSearchSerializer,
)


class AuthorTest(TestCase):

    def test_article_creation(self):
        Author.objects.create(
            name="My Author",
            picture="http://author.pic.com",
        )
        self.assertEqual(len(Author.objects.all()), 1)


class ArticleTest(TestCase):

    def test_article_creation(self):
        author = Author.objects.create(
            name="My Author",
            picture="http://author.pic.com",
        )
        Article.objects.create(
            author=author,
            category="Some category",
            title="Article title",
            summary="Article summary",
            first_paragraph="Article first paragraph",
            body="Article body",
        )
        self.assertEqual(len(Article.objects.all()), 1)


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


class ArticleListLoggedUserSerializerTest(TestCase):

    def test_article_list_serializer(self):
        author = Author.objects.create(name="Author 001", picture="http://picture.com")
        article = Article.objects.create(
            author=author,
            category="Category",
            title="Title",
            summary="Summary",
            first_paragraph="First paragraph",
            body="Body",
        )
        serializer = ArticleListLoggedUserSerializer(instance=article)

        self.assertEqual(str(article.author.id), serializer.data["author"]["id"])
        self.assertEqual(article.author.name, serializer.data["author"]["name"])
        self.assertEqual(article.author.picture, serializer.data["author"]["picture"])
        self.assertEqual(article.category, serializer.data["category"])
        self.assertEqual(article.title, serializer.data["title"])
        self.assertEqual(article.summary, serializer.data["summary"])
        self.assertEqual(article.first_paragraph, serializer.data["first_paragraph"])
        self.assertEqual(article.body, serializer.data["body"])


class ArticleListAnonymousUserSerializerTest(TestCase):

    def test_article_list_serializer(self):
        author = Author.objects.create(name="Author 001", picture="http://picture.com")
        article = Article.objects.create(
            author=author,
            category="Category",
            title="Title",
            summary="Summary",
            first_paragraph="First paragraph",
            body="Body",
        )
        serializer = ArticleListAnonymousUserSerializer(instance=article)

        self.assertEqual(str(article.author.id), serializer.data["author"]["id"])
        self.assertEqual(article.author.name, serializer.data["author"]["name"])
        self.assertEqual(article.author.picture, serializer.data["author"]["picture"])
        self.assertEqual(article.category, serializer.data["category"])
        self.assertEqual(article.title, serializer.data["title"])
        self.assertEqual(article.summary, serializer.data["summary"])
        self.assertEqual(article.first_paragraph, serializer.data["first_paragraph"])
        self.assertNotIn("body", serializer.data)


class ArticleListSearchSerializerTest(TestCase):

    def test_article_list_serializer(self):
        author = Author.objects.create(name="Author 001", picture="http://picture.com")
        article = Article.objects.create(
            author=author,
            category="Category",
            title="Title",
            summary="Summary",
            first_paragraph="First paragraph",
            body="Body",
        )
        serializer = ArticleListSearchSerializer(instance=article)

        self.assertEqual(str(article.author.id), serializer.data["author"]["id"])
        self.assertEqual(article.author.name, serializer.data["author"]["name"])
        self.assertEqual(article.author.picture, serializer.data["author"]["picture"])
        self.assertEqual(article.category, serializer.data["category"])
        self.assertEqual(article.title, serializer.data["title"])
        self.assertEqual(article.summary, serializer.data["summary"])
        self.assertNotIn("first_paragraph", serializer.data)
        self.assertNotIn("body", serializer.data)
