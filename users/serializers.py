from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer class to custom serialize token data.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise AuthenticationFailed('Invalid credentials.', code='invalid_credentials')
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled.', code='inactive_account')
            refresh = self.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email
            }
            return data
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authorization')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration of new user.
    """
    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        return user
    

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serializer custom user.
    """

    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'is_active',
            'status'
        )
    read_only_fields = ['date_joined',
                        'last_login']
    
    def get_status(self, obj):
        return 'Active' if obj.is_active else 'Inactive'