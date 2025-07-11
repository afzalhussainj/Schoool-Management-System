from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import *
from rest_enumfield import EnumField
from utils.enumerations import RoleChoices

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[]
    )
    profile_pic = serializers.ImageField(
        max_length=None,
        use_url=True,
        allow_null=True,
        required=False
        )

    def validate_email(self, value):
        if CustomUserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def create(self, validated_data):
        role = validated_data.pop('role', None)
        profile_pic = validated_data.pop('profile_pic', None)
        created_by = self.context.get('created_by')
        user = CustomUserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            created_by = created_by
            )
        if role:
            user.role = role
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        return user

    class Meta:
        model = CustomUserModel
        fields = ['email','password','profile_pic']


class CustomUserUpdateSerializer(CustomUserCreateSerializer):
    def update(self, instance, validated_data):

        for field,value in validated_data.items():
            setattr(instance,field,value)

        updated_by = self.context.get('updated_by')
        instance.updated_by = updated_by
        instance.save()
        return instance

    class Meta:
        model = CustomUserModel
        fields = ['email','profile_pic','role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.allow_null = True


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'})
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email,password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Wrong email or password.')
        else:
            raise serializers.ValidationError('Email or Password not provided.')
        return data
    
    class Meta:
        model = CustomUserModel
        fields = ['email','password'] 


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    role = EnumField(
        RoleChoices,
        to_repr=lambda x: RoleChoices(int(x)).name if isinstance(x, (str, int)) else x.name
    )
    
    class Meta:
        model = CustomUserModel
        fields = ['email','profile_pic','role'] 


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['email']

class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = CustomUserModel
        fields = ['old_password','new_password']
