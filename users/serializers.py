from rest_framework.exceptions import ValidationError

from . import models
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=6)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Пароль не найден')
        return data

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Пользователь уже существует')
        return username


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=5)


class SMSCodeSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6)