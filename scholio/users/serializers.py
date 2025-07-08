from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from utils.StandardResponse import standarizedErrorResponse,standarizedSuccessResponse
from drf_yasg.utils import swagger_auto_schema
from .models import *

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_pic = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
        )

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        profile_pic = validated_data.pop('profile_pic', None)
        request = self.context.get('request')
        created_by = request.user if request and request.user.is_authenticated else None
        user = CustomUserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            created_by = created_by,
            role = role
            )
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        return user

    class Meta:
        model = CustomUserModel
        fields = ['email','password','role','profile_pic']

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'})
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email,password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise ValidationError('Your account is disabled.')
            else:
                raise serializers.ValidationError('Wrong email or password.')
        else:
            raise serializers.ValidationError('Email or Password not provided.')
        return data
    
    class Meta:
        model = CustomUserModel
        fields = ['email','password'] 


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['email','profile_pic'] 
