from rest_framework import serializers
from .models import *

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        user = CustomUserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
            )
        if role:
            user.role = role
        user.save()
        return user

    class Meta:
        model = CustomUserModel
        fields = ['email','password','role']


# class PrincipalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Principal
#         fields = "__all__"

# class SchoolOwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SchoolOwner
#         fields = "__all__"

# class BranchManagerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BranchManager
#         fields = "__all__"