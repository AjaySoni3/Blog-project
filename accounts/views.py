from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from .models import CustomUser
from .renderers import UserRenderer
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer, \
    SendResetPasswordSerializer, UserResetPasswordSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate

from channels.layers import get_channel_layer
from django.http import HttpResponse
from asgiref.sync import async_to_sync

from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


""" API to activate user account """


class ActivateAPIView(APIView):
    def post(self, request, uid, token):
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a '
                                          'new one'},
                                status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.save()
            return Response({'success': 'User activated successfully'},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


activate = ActivateAPIView.as_view()

""" API to register user """


class RegisterAPIView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            tokens = get_tokens_for_user(user)
            return Response({"msg": "Email is sent to you to active your accounts", "tokens": tokens},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


register_api_view = RegisterAPIView.as_view()

""" API to login user """


class LoginAPIView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                tokens = get_tokens_for_user(user)
                return Response({"msg": "Login Succesfull", "tokens": tokens}, status=status.HTTP_200_OK)
            return Response({'error': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_api_view = LoginAPIView.as_view()

""" API to get user profile """


class UserProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


user_profile = UserProfile.as_view()

""" API to change user password """


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_change_password = UserChangePasswordView.as_view()

""" API to send reset password link """


class SendResetPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = SendResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Reset password link sent to your email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


send_reset_password = SendResetPasswordView.as_view()

""" API to reset password """


class UserResetPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token):
        serializer = UserResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_reset_password = UserResetPasswordView.as_view()

''' Google Auth API '''

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


google_login = GoogleLogin.as_view()

''' Test views '''


def test(request):
    message = "Hello World"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "test_group",
        {
            "type": "test_message",
            "message": "message"
        }
    )
    return HttpResponse("Hello World")
