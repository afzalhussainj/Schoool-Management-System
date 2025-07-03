from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.StandardResponse import (
    standarizedErrorResponse,
    standarizedSuccessResponse
    )
from utils.StandardResponse_serializers import (
    standarizedErrorResponseSerializer,
    standarizedSuccessResponseSerializer
    )
from .serializers import *
from .models import School
from .permissions import IsBranchManager,IsSchoolOwner

class SchoolAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = School.objects.filter(isdeleted=False)

    def get_queryset(self):
        return self.queryset.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        if self.request.method == 'GET':
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        request_body=SchoolSerializer,
        responses={
            201: openapi.Response(
                'Successfully created School.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to create School.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            created_school = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School "{created_school.name}"',
                status_code=status.HTTP_201_CREATED
            )
        return standarizedErrorResponse(
            details=serializer.errors,
            message='Failed to create school.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Successfully listed available School.',
                standarizedSuccessResponseSerializer
                ),
        }
    )
    def get(self, request):
        serializer = SchoolSerializer(self.get_queryset(),many=True)
        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully listed available School.',
            status_code=status.HTTP_200_OK
            )


class SchoolpkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = School.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [permissions.IsAdminUser()]
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Successfully Retrieved School.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            school = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND
                )
            
        serializer = SchoolSerializer(school)
        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available School.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                'Successfully Deleted School.',
                standarizedSuccessResponseSerializer
                ),
            404: openapi.Response(
                'Failed to delete school.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def delete(self, request, pk):
        try:
            school = self.queryset.objects.get(pk=pk)
        except School.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school.delete()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School "{school.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=SchoolSerializer,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                'Successfully updated school.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to update school.',
                standarizedErrorResponseSerializer
                ),
            404: openapi.Response(
                'School not found.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def put(self, request, pk):
        try:
            school = self.queryset.objects.get(pk=pk)
        except School.DoesNotExist:
            return standarizedErrorResponse(
                message="School doesn't exist.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            updated_school = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School "{updated_school.name}"',
                status_code=status.HTTP_200_OK
            )
        return standarizedErrorResponse(
            details=serializer.errors,
            message=f'Failed to update school "{school.name}".',
            status_code=status.HTTP_400_BAD_REQUEST
        )  


class SchoolBranchAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = SchoolBranch.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()|IsSchoolOwner]

    @swagger_auto_schema(
        request_body=SchoolBranchSerializer,
        responses={
            201: openapi.Response(
                'Successfully created School.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to create School.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def post(self, request):
        serializer = SchoolBranchSerializer(data=request.data)
        if serializer.is_valid():
            created_branch = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School branch"{created_branch.branch_name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create school branch.',
                status_code=status.HTTP_400_BAD_REQUEST)


class SchoolBranchpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = SchoolBranch.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [permissions.IsAdminUser()|IsSchoolOwner]
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()|IsSchoolOwner]
        if self.request.method == 'GET':
            return [permissions.AllowAny()]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Successfully Retrieved School Branch.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="Primary Key of the School Branch",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            branch = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School Branch.',
                status_code=status.HTTP_404_NOT_FOUND
                )
            
        serializer = SchoolSerializer(branch)

        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available School Branch.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School Branch", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully Deleted School Branch.', standarizedSuccessResponseSerializer),
            404: openapi.Response('Failed to delete school Branch.', standarizedErrorResponseSerializer),
        }
    )
    def delete(self, request, pk):
        try:
            branch = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to delete school Branch.',
                status_code=status.HTTP_404_NOT_FOUND)
        
        branch.isdeleted = True
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School Branch: "{branch.branch_name}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SchoolBranchSerializer,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the School Branch",
                type=openapi.TYPE_INTEGER
                )
        ],
        responses={
            200: openapi.Response(
                'Successfully updated school Branch.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to update school Branch.',
                standarizedErrorResponseSerializer
                ),
            404: openapi.Response(
                'School Branch not found.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def put(self, request, pk, format=None):
        try:
            current_branch = self.queryset.objects.get(pk=pk)
        except SchoolBranch.DoesNotExist:
            return standarizedErrorResponse(
                message="School branch does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolSerializer(current_branch, data=request.data)
        if serializer.is_valid():
            updated_branch = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School branch"{updated_branch.branch_name}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update school branch"{current_branch.branch_name}".',
                status_code=status.HTTP_400_BAD_REQUEST)

