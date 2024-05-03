from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        email = attrs.get('email', '')
        if models.User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already in use')

        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    full_name = serializers.CharField(max_length=68, read_only=True)
    access_tokens = serializers.CharField(max_length=255, read_only=True)
    refresh_tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'password', 'full_name', 'access_tokens', 'refresh_tokens')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        user_tokens = user.tokens()

        return {
            "email": user.email,
            "full_name": user.get_full_name,
            "access_tokens": str(user_tokens.get('access')),
            "refresh_tokens": str(user_tokens.get('refresh'))
        }

