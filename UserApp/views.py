from django.shortcuts import render
from djoser.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet

from UserApp.models import User


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
