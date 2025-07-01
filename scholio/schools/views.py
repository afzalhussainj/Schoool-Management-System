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

class SchoolRetrieveAllAPIview(APIView):
    # queryset = School.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully Retrieved available Schools.'),
            }
    )

    def get(self, request):
        queryset = School.objects.all()
        serialized_data = SchoolSerializer(data=queryset,many=True)
        return StandarizedSuccessResponse(
            data=serialized_data.data,
            message=f'Successfully retrieved available Schools.',
                status_code=status.HTTP_200_OK)
    
class SchoolRetrieveSpecificAPIview(APIView):
    # queryset = School.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to retrieve School.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully retrieved School.'),
            }
    )
    def get(self,pk, request):
        queryset = School.objects.get(pk=pk)
        if queryset:
            serialized_data = SchoolSerializer(data=queryset)
            return StandarizedSuccessResponse(
                data=serialized_data.data,
                message=f'Successfully Retrieved School "{queryset.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                message='Failed to retrieve school.',
                status_code=status.HTTP_404_NOT_FOUND)

class SchoolDeleteAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to delete school.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully Deleted School.'),
            }
    )
    def delete(self,pk, request):
        queryset = School.objects.get(pk=pk)
        if queryset:
            name = queryset.name
            queryset.delete()
            return StandarizedSuccessResponse(
                message=f'Successfully Deleted School "{name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND)

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

class SchoolBranchRetrieveAllAPIview(APIView):
    # queryset = School.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolBranchSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully Retrieved available School Branches.'),
            }
    )

    def get(self, request):
        queryset = SchoolBranch.objects.all()
        serialized_data = SchoolBranchSerializer(data=queryset,many=True)
        return StandarizedSuccessResponse(
            data=serialized_data.data,
            message=f'Successfully retrieved available School Branches.',
                status_code=status.HTTP_200_OK)

class SchoolBranchRetrieveAllSpecificAPIview(APIView):
    # queryset = School.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolBranchSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully Retrieved available School Branches.'),
            }
    )

    def get(self,pk, request):
        queryset = SchoolBranch.objects.get(school=School.objects.get(pk=pk))
        serialized_data = SchoolBranchSerializer(data=queryset,many=True)
        return StandarizedSuccessResponse(
            data=serialized_data.data,
            message=f'Successfully retrieved available School Branches.',
                status_code=status.HTTP_200_OK)
    
class SchoolBranchRetrieveSpecificAPIview(APIView):
    # queryset = School.objects.all()
    # permission_classes = [permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolBranchSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to retrieve School Branch.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully retrieved School Branch.'),
            }
    )
    def get(self,pk, request):
        queryset = SchoolBranch.objects.get(pk=pk)
        if queryset:
            serialized_data = SchoolBranchSerializer(data=queryset)
            return StandarizedSuccessResponse(
                data=serialized_data.data,
                message=f'Successfully Retrieved School Branch: "{queryset.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                message='Failed to retrieve school Branch.',
                status_code=status.HTTP_404_NOT_FOUND)

class SchoolBranchDeleteAPIview(APIView):
    # queryset = School.objects.all()
    permission_classes = [permissions.IsAdminUser,IsSchoolOwner]
    authentication_classes = [JWTAuthentication]
    serializer_class = SchoolBranchSerializer

    @extend_schema(
            # methods=["POST"],
            request=SchoolBranchSerializer,
            # parameters=OpenApiParameter(name='access_token')
            responses={
                404:OpenApiResponse(StandarizedErrorResponseSerializer,description='Failed to delete school branch.'),
                200:OpenApiResponse(StandarizedSuccessResponseSerializer,description='Successfully Deleted School branch.'),
            }
    )
    def delete(self,pk, request):
        queryset = SchoolBranch.objects.get(pk=pk)
        if queryset:
            name = queryset.name
            queryset.delete()
            return StandarizedSuccessResponse(
                message=f'Successfully Deleted School Branch: "{name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                message='Failed to delete school Branch.',
                status_code=status.HTTP_404_NOT_FOUND)

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