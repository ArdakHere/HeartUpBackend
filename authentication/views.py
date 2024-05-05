from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from . import models
from .utils import send_otp_email


class RegisterUserView(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            user = serializer.data

            # send email with email verification code
            send_otp_email(user['email'])

            return Response({
                'data': user,
                'message': 'User created successfully. Check your email to verify your account'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'error': serializer.errors,
            'message': 'Validation Error. Please check your data and try again.'
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(generics.GenericAPIView):
    queryset = models.OneTimePassword.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = models.OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user

            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': 'User email verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'User email already verified'
            }, status=status.HTTP_204_NO_CONTENT)
        except models.OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Invalid OTP code'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            return Response({'access': new_access_token}, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TestAuthenticationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'You are authenticated'
        }, status=status.HTTP_200_OK)


# START OF Password reset views ========================================
class PasswordResetRequestView(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message': 'a link to reset your password has been sent to your email address'
            },
            status=status.HTTP_200_OK
        )


class PasswordResetConfirm(generics.GenericAPIView):
    queryset = models.User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'message': 'Invalid token or the token has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {
                    'success': True,
                    'message': 'Credentials are valid',
                    'uidb64': uidb64,
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        except DjangoUnicodeDecodeError:
            return Response(
                {'message': 'Invalid token or the token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )


class SetNewPassword(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'message': 'Password reset successful'
            },
            status=status.HTTP_200_OK
        )


# END of Password reset views ==========================================


class LogoutUserView(generics.GenericAPIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
