from django.shortcuts import render
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    CustomUserSerializer
)

User = get_user_model()

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for setting page size and maximum page size.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomTokenPairView(TokenObtainPairView):
    """
    Custom view for obtaining a JWT token pair (access and refresh tokens).
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        """
        Handle POST request to obtain token pair.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        response = {
            "success": True,
            "status code": status.HTTP_200_OK,
            "message": "User logged in successfully",
            "email": serializer.validated_data["email"],
            "refresh": serializer.validated_data["refresh"],
            "access": serializer.validated_data["access"],
        }
        return Response(response, status=status.HTTP_200_OK)
    

class UserDetailsView(APIView):
    """
    View for retrieving details of the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        """
        Handle GET request to retrieve user details.
        """
        serializer = self.serializer_class(request.user)
        user_data = serializer.data
        return Response(data=user_data, status=status.HTTP_200_OK)
    

class RegisterView(CreateAPIView):
    """
    View for registering a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request to register a new user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "success": True,
            "status code": status.HTTP_200_OK,
            "message": "User registered successfully",
        }
        return Response(response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    View for logging out the authenticated user.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to log out the user by blacklisting the refresh token.
        """
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token, verify=False)
            token.blacklist()

            user = request.user
            user.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserListView(ListAPIView):
    """
    View for listing and creating users with pagination and filtering options.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Customize the queryset to support filtering by email and status.
        """
        queryset = User.objects.order_by('-date_joined')
        email = self.request.query_params.get('email')
        status = self.request.query_params.get('status')
        
        if email:
            queryset = queryset.filter(email__icontains=email)
        if status:
            queryset = queryset.filter(is_active=(status.lower() == 'active'))
        return queryset
