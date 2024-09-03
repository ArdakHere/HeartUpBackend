from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, OutstandingToken

from . import models
from .utils import send_normal_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')


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
    user_id = serializers.CharField(max_length=68, read_only=True)
    role = serializers.CharField(max_length=68, read_only=True)
    access_tokens = serializers.CharField(max_length=255, read_only=True)
    refresh_tokens = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'password', 'full_name', 'user_id', 'role', 'access_tokens', 'refresh_tokens')

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
            "user_id": user.id,
            "role": user.role,
            "access_tokens": str(user_tokens.get('access')),
            "refresh_tokens": str(user_tokens.get('refresh'))
        }


# Serializer for requesting a password reset
# This serializer will validate the email and send a link to the user's email
# The link will contain a token that will be used to reset the password
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = models.User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            request = self.context.get('request')

            site_domain = get_current_site(request).domain
            relative_link = reverse(
                'password-reset-confirm',
                kwargs={'uidb64': uidb64, 'token': token}
            )
            abs_url = f'http://{site_domain}{relative_link}'

            email_body = f"Hi use the link below to reset your password\n {abs_url}"
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password'
            }
            send_normal_email(data)

            return super().validate(attrs)


# Serializer for setting a new password
# This serializer will validate the new password and confirm password
# It will also validate the token and uidb64
# If the token is valid, the user's password will be updated
class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    confirm_password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('password', 'confirm_password', 'uidb64', 'token')

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('The reset link is invalid', code=400)

            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            if password != confirm_password:
                raise serializers.ValidationError('Passwords do not match', code=400)

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('The reset link is expired', code=400)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
            OutstandingToken.objects.filter(user_id=token['user_id']).delete()
        except TokenError:
            self.fail('bad_token')
