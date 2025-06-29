# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from schools.serializers import SchoolSerializer
from schools.models import School
from .models import Principal
from .serializers import *
from rest_framework.views import APIView
from ..utils.StandardResponse import StandarizedErrorResponse, StandarizedSuccessResponse
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

class SchoolAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            created_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School "{created_school.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create school.',
                status_code=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        try:
            current_school = self.get_object(pk)
        except School.DoesNotExist:
            return StandarizedErrorResponse(
                message="School does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(current_school, data=request.data)
        if serializer.is_valid():
            updated_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School "{updated_school.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update school "{current_school.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)

class BranchManagerAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser, IsSchoolOwner]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = BranchManagerSerializer(data=request.data)
        if serializer.is_valid():
            created_bm = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Branch Manager "{created_bm.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Branch manager.',
                status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            current_bm = self.get_object(pk)
        except BranchManager.DoesNotExist:
            return StandarizedErrorResponse(
                message="Branch Manager does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = BranchManagerSerializer(current_bm, data=request.data)
        if serializer.is_valid():
            updated_bm = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Branch Manager "{updated_bm.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
    
class PrincipalCreateAPIview(APIView):
    # queryset = Principal.objects.all()
    # serializer_class = PrincipalSerializer
    authentication_classes = [permissions.IsAdminUser, IsBranchManager, IsSchoolOwner]

    def post(self, request):
        serializer = PrincipalSerializer(data=request.data)
        if serializer.is_valid():
            created_principal = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Principal "{created_principal.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Principal.',
                status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            current_principal = self.get_object(pk)
        except Principal.DoesNotExist:
            return StandarizedErrorResponse(
                message="Principal does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = PrincipalSerializer(current_principal, data=request.data)
        if serializer.is_valid():
            updated_principal = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Principal "{updated_principal.get('name')}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update principal "{current_principal.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 