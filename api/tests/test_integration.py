from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Article, Author


class SignUpLoginTestCase(APITestCase):
    def setUp(self):
        self.username = "admin"
        self.password = "asdf!@#$"
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()
        self.admin_token = Token.objects.create(user=user)

    def test_create_account(self):
        """Ensure we are able to create new accoutns.
        """
        data = {
            "username": "new_user1",
            "password": "new_user1_password",
        }
        response = self.client.post(reverse("sign-up"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "username": "new_user2",
            "password": "new_user2_password",
        }
        response = self.client.post(reverse("sign-up"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_with_existent_user(self):
        """Ensure we cannot create an account using an already used username .
        """
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(reverse("sign-up"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_an_existing_user(self):
        """We are able to log in with valid user credentials.
        """
        data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], str(self.admin_token))

    def test_login_with_invalid_credentials(self):
        """We're not able to log in with invalid credentials.
        """
        data = {
            "username": "invalid_username",
            "password": self.password,
        }
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthorAdminTestCase(APITestCase):
    def setUp(self):
        self.credentials = {
            "username": "admin",
            "password": "adminpasswd"
        }
        response = self.client.post(reverse("sign-up"), self.credentials)
        response = self.client.post(reverse("login"), self.credentials)
        self.auth_token = response.data["token"]

    def test_new_author_create(self):
        """When you have a valid and logged user you're able to create authors.
        """
        data = {
            "name": "Author 001",
            "picture": "http://author001.picture.com",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-authors"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["picture"], data["picture"])

    def test_new_author_create_with_invalid_url(self):
        """When you don't specify a valid URL attempts to create authors won't succeed.
        """
        data = {
            "name": "Author 001",
            "picture": "some.invalid.url",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-authors"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_author_create_with_invalid_access_token(self):
        """When you don't have a valid token attempts to create authors won't succeed.
        """
        data = {
            "name": "Author 001",
            "picture": "http://author001.picture.com",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "my-invali-token")
        response = self.client.post(reverse("admin-authors"), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_authors_list(self):
        """Logged users are able to get all authors records.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)

        response = self.client.get(reverse("admin-authors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        for i in range(3):
            data = {"name": f"Author {i}", "picture": f"http://author{i}pic.com"}
            response = self.client.post(reverse("admin-authors"), data)

        response = self.client.get(reverse("admin-authors"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_authors_list_with_not_logged_user(self):
        """Users that are not logged cannot access the authos data.
        """
        response = self.client.get(reverse("admin-authors"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_author_info(self):
        """With an id of an existent author we can retreive its information.
        """
        data = {
            "name": "Author",
            "picture": "http://author.com"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-authors"), data)
        author_id = response.data["id"]
        response = self.client.get(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(author_id, response.data["id"])
        self.assertEqual(data["name"], response.data["name"])
        self.assertEqual(data["picture"], response.data["picture"])

    def test_get_single_author_with_invalid_access_token(self):
        """When you don't have a valid token attempts to read authors won't succeed.
        """
        author_id = "here-it-doesnt-matter"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "my-invali-token")
        response = self.client.get(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_author_with_invalid_id(self):
        """No author will be found if we use an non existend id.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        author_id = "f2dead5209b494683c7c0bb2bfc965b6ecf754a2"
        response = self.client.get(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_author_info(self):
        """We are able to update an author info of an existent author.
        """
        data = {
            "name": "Author",
            "picture": "http://author.com"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-authors"), data)
        author_id = response.data["id"]
        data["name"] = "New Author Name"
        data["picture"] = "http://newauthorpic.com"
        response = self.client.put(reverse("admin-authors-id", args=[author_id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], response.data["name"])
        self.assertEqual(data["picture"], response.data["picture"])

    def test_update_author_with_invalid_access_token(self):
        """When you don't have a valid token attempts to update authors won't succeed.
        """
        author_id = "here-it-doesnt-matter"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "my-invali-token")
        response = self.client.put(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_author_with_invalid_id(self):
        """No author will be found if we use an non existend id.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        author_id = "f2dead5209b494683c7c0bb2bfc965b6ecf754a2"
        response = self.client.put(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_author(self):
        """We are able to delete authors records.
        """
        data = {
            "name": "My Author",
            "picture": "https://myauthorpic.com"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-authors"), data)
        author_id = response.data["id"]
        response = self.client.get(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_author_with_invalid_access_token(self):
        """When you don't have a valid token attempts to delete authors won't succeed.
        """
        author_id = "here-it-doesnt-matter"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "my-invali-token")
        response = self.client.delete(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_author_with_invalid_id(self):
        """No author will be found if we use an non existend id.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        author_id = "f2dead5209b494683c7c0bb2bfc965b6ecf754a2"
        response = self.client.delete(reverse("admin-authors-id", args=[author_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ArticleAdminTestCase(APITestCase):
    def setUp(self):
        self.credentials = {
            "username": "admin",
            "password": "adminpasswd"
        }
        self.author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        response = self.client.post(reverse("sign-up"), self.credentials)
        response = self.client.post(reverse("login"), self.credentials)
        self.auth_token = response.data["token"]

    def test_create_new_article(self):
        """When we use correct information an article is successfully created.
        """
        data = {
            "author": self.author.id,
            "category": "Article category",
            "title": "Article title",
            "summary": "Article summary",
            "first_paragraph": "Article first paragraph",
            "body": "Article body"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-articles"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_new_article_with_invalid_author_id(self):
        """We are not able to create an article with an invalid author id.
        """
        data = {
            "author": "b6d1a41a-invalid-author-id-f888a2dcf",
            "category": "Article category",
            "title": "Article title",
            "summary": "Article summary",
            "first_paragraph": "Article first paragraph",
            "body": "Article body"
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.post(reverse("admin-articles"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_article_with_invalid_credentials(self):
        """With invalid credentials we are not able to create new articles.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "invalid-token")
        response = self.client.post(reverse("admin-articles"), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_articles_list(self):
        """With the right credentials, we are able to get a list of articles.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)

        response = self.client.get(reverse("admin-articles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        for i in range(3):
            Article.objects.create(
                author=author,
                category=f"some category 00{i}",
                title="some title 00{i}",
            )

        response = self.client.get(reverse("admin-articles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_article_by_id(self):
        """We are able to get a specific article with its id.
        """
        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        article = Article.objects.create(
            author=author,
            category="some category",
            title="some title",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.get(reverse("admin-articles-id", args=[article.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(article.id))

    def test_get_article_by_id_with_invalid_credentials(self):
        """We are not able to get a specific article with invalid credentials.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "invalid-token")
        response = self.client.get(reverse("admin-articles-id", args=["we-wont-get-here"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_article_by_id_with_invalid_id(self):
        """We are not able to get a specific article with invalid credentials.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.get(reverse("admin-articles-id", args=["invalid-id"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article_info(self):
        """With the right credentials and id we are able to update an article info.
        """
        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        article = Article.objects.create(
            author=author,
            category="some category",
            title="some title",
            summary="summary",
            first_paragraph="first paragraph",
            body="body"
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        data = {
            "author": str(author.id),
            "category": article.category + " (updated)",
            "title": article.title + " (updated)",
            "summary": article.summary,
            "first_paragraph": article.first_paragraph,
            "body": article.body,
        }
        response = self.client.put(reverse("admin-articles-id", args=[article.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category"], data["category"])
        self.assertEqual(response.data["summary"], data["summary"])

    def test_update_article_info_with_invalid_author_id(self):
        """With the right credentials and id we are able to update an article info.
        """
        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        article = Article.objects.create(
            author=author,
            category="some category",
            title="some title",
            summary="summary",
            first_paragraph="first paragraph",
            body="body"
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        data = {
            "author": "some-invalid-id",
            "category": article.category + " (updated)",
            "title": article.title + " (updated)",
            "summary": article.summary,
            "first_paragraph": article.first_paragraph,
            "body": article.body,
        }
        response = self.client.put(reverse("admin-articles-id", args=[article.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_article_info_with_new_author_id(self):
        """We are able to move an article from a author to other.
        """
        author1 = Author.objects.create(name="Author 01", picture="http://author1pic.com")
        author2 = Author.objects.create(name="Author 02", picture="http://author2pic.com")

        article = Article.objects.create(
            author=author1,
            category="some category",
            title="some title",
            summary="summary",
            first_paragraph="first paragraph",
            body="body"
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        data = {
            "author": str(author2.id),
            "category": article.category,
            "title": article.title,
            "summary": article.summary,
            "first_paragraph": article.first_paragraph,
            "body": article.body,
        }
        response = self.client.put(reverse("admin-articles-id", args=[article.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        article = Article.objects.get(id=article.id)
        self.assertEqual(article.author.id, author2.id)

    def test_delete_article(self):
        """With the right credentials and id we are able to update an article info.
        """
        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        article = Article.objects.create(
            author=author,
            category="some category",
            title="some title",
            summary="summary",
            first_paragraph="first paragraph",
            body="body"
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.auth_token)
        response = self.client.delete(reverse("admin-articles-id", args=[article.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse("admin-articles-id", args=[article.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ArticleListTestCase(APITestCase):
    def setUp(self):
        author = Author.objects.create(name="Some Author", picture="http://authorpic.com")
        Article.objects.create(
            author=author,
            category="some category",
            title="some title 001",
            summary="summary 001",
            first_paragraph="first paragraph 001",
            body="body 001"
        )
        Article.objects.create(
            author=author,
            category="some category",
            title="some title 002",
            summary="summary 002",
            first_paragraph="first paragraph 002",
            body="body 002"
        )
        Article.objects.create(
            author=author,
            category="other category",
            title="some title 003",
            summary="summary 003",
            first_paragraph="first paragraph 003",
            body="body 003"
        )

    def test_list_article_search_all(self):
        response = self.client.get(reverse("articles-search"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
