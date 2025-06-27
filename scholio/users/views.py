# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from schools.serializers import SchoolsSerializer
from schools.models import School
from .models import Principal
from .serializers import *
from rest_framework.views import APIView
from ..utils.ResponseFormat import JsonFormatedResponse
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

class SchoolCreateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = SchoolsSerializer(data=request.data)
        if serializer.is_valid():
            return JsonFormatedResponse(data=serializer.data,message='',status=status.HTTP_201_CREATED)
        
class BranchManagerCreateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser, IsSchoolOwner]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = BranchManagerSerializer(data=request.data)
        if serializer.is_valid():
            return JsonFormatedResponse(data=serializer.data,message='',status=status.HTTP_201_CREATED)



class PrincipalCreateAPIview(APIView):
    # queryset = Principal.objects.all()
    # serializer_class = PrincipalSerializer
    authentication_classes = [permissions.IsAdminUser, IsBranchManager, IsSchoolOwner]

    def post(self, request):
        serializer = BranchManagerSerializer(data=request.data)
        if serializer.is_valid():
            return JsonFormatedResponse(data=serializer.data,message='',status=status.HTTP_201_CREATED)
