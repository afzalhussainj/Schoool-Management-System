from . models import *
from rest_framework import serializers

class SchoolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'