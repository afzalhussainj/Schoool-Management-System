# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions
from schools.serializers import SchoolsSerializer
from schools.models import School
from .models import Principal
from .serializers import PrincipalSerializer
# Create your views here.

class SchoolCreateiew(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolsSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

class PrincipalCreateiew(generics.CreateAPIView):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    authentication_classes = [permissions.IsAdminUser]