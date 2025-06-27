from . models import *
from rest_framework import serializers

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class SchoolBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolBranch
        fields = '__all__'