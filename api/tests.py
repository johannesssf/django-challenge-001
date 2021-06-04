from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class SignUpLoginTestCase(APITestCase):
    def setUp(self):
        self.username="admin"
        self.password="asdf!@#$"
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
