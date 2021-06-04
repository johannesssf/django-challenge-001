from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView

from .serialyzes import UserSerialyzer


class UserSignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialyzer
    lookup_field = "username"
