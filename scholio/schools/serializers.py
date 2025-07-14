from . models import *
from rest_framework import serializers

class SchoolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class SchoolBranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolBranch
        fields = '__all__'