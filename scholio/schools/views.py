from django.shortcuts import render
from .serializers import SchoolSerializer
from .models import School
from rest_framework.views import APIView
from .permissions import IsBranchManager,IsSchoolOwner
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.StandardResponse import StandarizedErrorResponse,StandarizedSuccessResponse
from rest_framework import status

# Create your views here.

class SchoolAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            created_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School "{created_school.name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create school.',
                status_code=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        try:
            current_school = School.objects.get(pk=pk)
        except School.DoesNotExist:
            return StandarizedErrorResponse(
                message="School does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(current_school, data=request.data)
        if serializer.is_valid():
            updated_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School "{updated_school.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update school "{current_school.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)