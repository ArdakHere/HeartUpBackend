from rest_framework import generics, status, permissions
from rest_framework.response import Response
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
            'data': 'Validation Error. Please check your data and try again.'
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


class TestAuthenticationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'message': 'You are authenticated'
        }, status=status.HTTP_200_OK)
