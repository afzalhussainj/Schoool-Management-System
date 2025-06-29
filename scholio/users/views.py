# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from .models import Principal
from .serializers import *
from rest_framework.views import APIView
from utils.StandardResponse import StandarizedErrorResponse, StandarizedSuccessResponse
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

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
                message=f'Successfully created Branch Manager "{created_bm.name}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Branch manager.',
                status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            current_bm = BranchManager.objects.get(pk=pk)
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
                status=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
    
class PrincipalAPIview(APIView):
    # queryset = Principal.objects.all()
    # serializer_class = PrincipalSerializer
    permission_classes = [permissions.IsAdminUser, IsBranchManager, IsSchoolOwner]

    def post(self, request):
        serializer = PrincipalSerializer(data=request.data)
        if serializer.is_valid():
            created_principal = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Principal "{created_principal.name}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Principal.',
                status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            current_principal = Principal.objects.get(pk=pk)
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
                status=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update principal "{current_principal.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 
class OwnerAPIview(APIView):
    # queryset = Principal.objects.all()
    # serializer_class = PrincipalSerializer
    permission_classes = [permissions.IsAdminUser, IsBranchManager, IsSchoolOwner]

    def post(self, request):
        serializer = SchoolOwnerSerializer(data=request.data)
        if serializer.is_valid():
            created_owner = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Owner "{created_owner.name}"',
                status=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Owner.',
                status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        try:
            current_owner = SchoolOwner.objects.get(pk=pk)
        except SchoolOwner.DoesNotExist:
            return StandarizedErrorResponse(
                message="Owner does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = PrincipalSerializer(current_owner, data=request.data)
        if serializer.is_valid():
            updated_owner = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Owner "{updated_owner.get('name')}"',
                status=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Owner "{current_owner.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 