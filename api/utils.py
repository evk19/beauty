from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    user.auth_token.delete()
    if user is None:
        raise serializers.ValidationError(
            "Invalid email/password. Please try again!")
    return user


def create_user_account(email, password, name="",
                        surname="", **extra_fields):
    user = get_user_model().objects.create_user(
        email=email, password=password, name=name,
        surname=surname, **extra_fields)
    return user
