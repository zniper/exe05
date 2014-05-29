from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


def authenticate_email(email, password):
    """ Verify credential using email instead of username """
    try:
        user = User.objects.get(email=email)
        return user.check_password(password)
    except User.DoesNotExist:
        pass
    return False


class Authenticate(APIView):

    def get(self, request, format=None):
        email = request.GET.get('email', '').lower()
        password = request.GET.get('password', '')
        # get the user and try to authenticate
        result = 'success' if authenticate_email(email, password) else 'failed'
        return Response({'result': result})


class Register(CreateAPIView):

    model = User

    def post_save(self, obj, created=False):
        """ Just for encrypting the password """
        if created:
            obj.set_password(obj.password)
            obj.save()
