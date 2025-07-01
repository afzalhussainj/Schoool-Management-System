from django.shortcuts import render
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import OpenApiResponse,extend_schema
from utils.StandardResponse import StandarizedErrorResponse,StandarizedSuccessResponse
from utils.StandardResponse_serializers import StandarizedErrorResponseSerializer,StandarizedSuccessResponseSerializer
from .serializers import *
from .models import School
from .permissions import IsBranchManager,IsSchoolOwner

# Create your views here.

class SchoolCreateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to create School.'),
                201:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully created School.'),
            }
    )
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

class SchoolUpdateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    @extend_schema(
            methods=["PUT"],
            # auth=['JWTAuthentication'],
            request=SchoolSerializer,
            responses={
                400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to update school.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successful.'),
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='School not found.'),
            }
    )  
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

class SchoolBranchCreateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser,IsSchoolOwner]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolBranchSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to create School.'),
                201:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully created School.'),
            }
    )
    def post(self, request):
        serializer = SchoolBranchSerializer(data=request.data)
        if serializer.is_valid():
            created_branch = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School branch"{created_branch.branch_name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create school branch.',
                status_code=status.HTTP_400_BAD_REQUEST)

class SchoolBranchUpdateAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser,IsSchoolOwner]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            methods=["PUT"],
            # auth=['JWTAuthentication'],
            request=SchoolBranchSerializer,
            responses={
                400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to update school branch.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successful.'),
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='School branch not found.'),
            }
    )  
    def put(self, request, pk, format=None):
        try:
            current_branch = SchoolBranch.objects.get(pk=pk)
        except SchoolBranch.DoesNotExist:
            return StandarizedErrorResponse(
                message="School branch does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(current_branch, data=request.data)
        if serializer.is_valid():
            updated_branch = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School branch"{updated_branch.branch_name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update school branch"{current_branch.branch_name}".',
                status_code=status.HTTP_400_BAD_REQUEST)

#combined api view classes
# class SchoolAPIview(APIView):
#     # queryset = School.objects.all()
#     permission_classes = [permissions.IsAdminUser]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = SchoolSerializer

#     @extend_schema(
#             # methods=["POST"],
#             request=SchoolSerializer,
#             # parameters=OpenApiParameter(name='access_token')
#             responses={
#                 400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to create School.'),
#                 201:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully created School.'),
#             }
#     )
#     def post(self, request):
#         serializer = SchoolSerializer(data=request.data)
#         if serializer.is_valid():
#             created_school = serializer.save()
#             return StandarizedSuccessResponse(
#                 data=serializer.data,
#                 message=f'Successfully created School "{created_school.name}"',
#                 status_code=status.HTTP_201_CREATED)
#         else:
#             return StandarizedErrorResponse(
#                 details=serializer.errors,
#                 message='Failed to create school.',
#                 status_code=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#             methods=["PUT"],
#             # auth=['JWTAuthentication'],
#             request=SchoolSerializer,
#             responses={
#                 400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to update school.'),
#                 200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successful.'),
#                 404:OpenApiResponse(StandarizedErrorResponseSerializer,description='School not found.'),
#             }
#     )  
#     def put(self, request, pk, format=None):
#         try:
#             current_school = School.objects.get(pk=pk)
#         except School.DoesNotExist:
#             return StandarizedErrorResponse(
#                 message="School does'nt exist.",
#                 status_code=status.HTTP_404_NOT_FOUND)
#         serializer = SchoolSerializer(current_school, data=request.data)
#         if serializer.is_valid():
#             updated_school = serializer.save()
#             return StandarizedSuccessResponse(
#                 data=serializer.data,
#                 message=f'Successfully updated School "{updated_school.name}"',
#                 status_code=status.HTTP_200_OK)
#         else:
#             return StandarizedErrorResponse(
#                 details=serializer.errors,
#                 message=f'Failed to update school "{current_school.name}".',
#                 status_code=status.HTTP_400_BAD_REQUEST)

# class SchoolBranchAPIview(APIView):
#     # queryset = School.objects.all()
#     permission_classes = [permissions.IsAdminUser,IsSchoolOwner]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = SchoolBranchSerializer

#     @extend_schema(
#             # methods=["POST"],
#             request=SchoolBranchSerializer,
#             # parameters=OpenApiParameter(name='access_token')
#             responses={
#                 400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to create School.'),
#                 201:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully created School.'),
#             }
#     )
#     def post(self, request):
#         serializer = SchoolBranchSerializer(data=request.data)
#         if serializer.is_valid():
#             created_branch = serializer.save()
#             return StandarizedSuccessResponse(
#                 data=serializer.data,
#                 message=f'Successfully created School branch"{created_branch.branch_name}"',
#                 status_code=status.HTTP_201_CREATED)
#         else:
#             return StandarizedErrorResponse(
#                 details=serializer.errors,
#                 message='Failed to create school branch.',
#                 status_code=status.HTTP_400_BAD_REQUEST)

#     @extend_schema(
#             methods=["PUT"],
#             # auth=['JWTAuthentication'],
#             request=SchoolBranchSerializer,
#             responses={
#                 400:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to update school branch.'),
#                 200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successful.'),
#                 404:OpenApiResponse(StandarizedErrorResponseSerializer,description='School branch not found.'),
#             }
#     )  
#     def put(self, request, pk, format=None):
#         try:
#             current_branch = SchoolBranch.objects.get(pk=pk)
#         except SchoolBranch.DoesNotExist:
#             return StandarizedErrorResponse(
#                 message="School branch does'nt exist.",
#                 status_code=status.HTTP_404_NOT_FOUND)
#         serializer = SchoolSerializer(current_branch, data=request.data)
#         if serializer.is_valid():
#             updated_branch = serializer.save()
#             return StandarizedSuccessResponse(
#                 data=serializer.data,
#                 message=f'Successfully updated School branch"{updated_branch.branch_name}"',
#                 status_code=status.HTTP_200_OK)
#         else:
#             return StandarizedErrorResponse(
#                 details=serializer.errors,
#                 message=f'Failed to update school branch"{current_branch.branch_name}".',
#                 status_code=status.HTTP_400_BAD_REQUEST)