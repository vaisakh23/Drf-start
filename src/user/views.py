from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'message': 'Login successful',
            'username': f'{user.username}',
            'token': f'{token.key}'
        }
        return Response(response)


class UserLogoutView(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]
    
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        response = {
            'message': 'Logout successful',
            'username': f'{request.user.username}'
        }
        return Response(response)


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            'message': 'registration successful',
            'username': f'{user.username}'
        }
        return Response(response)


class DetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]


