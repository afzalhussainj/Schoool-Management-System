from rest_framework import serializers
from .models import *

class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = "__all__"

class SchoolOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolOwner
        fields = "__all__"

class BranchManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchManager
        fields = "__all__"