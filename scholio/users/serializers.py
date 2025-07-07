from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from utils.StandardResponse import standarizedErrorResponse,standarizedSuccessResponse
from drf_yasg.utils import swagger_auto_schema
from .models import *

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        request = self.context.get('request')
        created_by = request.user if request and request.user.is_authenticated else None
        user = CustomUserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            created_by = created_by
            )
        if role:
            user.role = role
        user.save()
        return user

    class Meta:
        model = CustomUserModel
        fields = ['email','password','role']

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
        fields = ['email'] 
