from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.StandardResponse import StandarizedErrorResponse,StandarizedSuccessResponse
from utils.StandardResponse_serializers import StandarizedErrorResponseSerializer,StandarizedSuccessResponseSerializer
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
            201: openapi.Response('Successfully created School.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to create School.', StandarizedErrorResponseSerializer),
        }
    )
    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            created_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created School "{created_school.name}"',
                status_code=status.HTTP_201_CREATED
            )
        return StandarizedErrorResponse(
            details=serializer.errors,
            message='Failed to create school.',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Successfully listed available School.', StandarizedSuccessResponseSerializer),
        }
    )
    def get(self, request):
        serializer = SchoolSerializer(self.get_queryset(),many=True)
        return StandarizedSuccessResponse(
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
            200: openapi.Response('Successfully Retrieved School.',StandarizedSuccessResponseSerializer),
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
            return StandarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND
                )
            
        serializer = SchoolSerializer(school)
        return StandarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available School.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully Deleted School.', StandarizedSuccessResponseSerializer),
            404: openapi.Response('Failed to delete school.', StandarizedErrorResponseSerializer),
        }
    )
    def delete(self, request, pk):
        try:
            school = self.queryset.objects.get(pk=pk)
        except School.DoesNotExist:
            return StandarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school.delete()
        return StandarizedSuccessResponse(
            message=f'Successfully Deleted School "{school.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=SchoolSerializer,
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully updated school.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to update school.', StandarizedErrorResponseSerializer),
            404: openapi.Response('School not found.', StandarizedErrorResponseSerializer),
        }
    )
    def put(self, request, pk):
        try:
            school = self.queryset.objects.get(pk=pk)
        except School.DoesNotExist:
            return StandarizedErrorResponse(
                message="School doesn't exist.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = SchoolSerializer(school, data=request.data)
        if serializer.is_valid():
            updated_school = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School "{updated_school.name}"',
                status_code=status.HTTP_200_OK
            )
        return StandarizedErrorResponse(
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
            201: openapi.Response('Successfully created School.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to create School.', StandarizedErrorResponseSerializer),
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
            200: openapi.Response('Successfully Retrieved School Branch.',StandarizedSuccessResponseSerializer),
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
            return StandarizedErrorResponse(
                message='Failed to retrieve School Branch.',
                status_code=status.HTTP_404_NOT_FOUND
                )
            
        serializer = SchoolSerializer(branch)

        return StandarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available School Branch.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School Branch", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully Deleted School Branch.', StandarizedSuccessResponseSerializer),
            404: openapi.Response('Failed to delete school Branch.', StandarizedErrorResponseSerializer),
        }
    )
    def delete(self, request, pk):
        try:
            branch = self.queryset.objects.get(pk=pk)
        except:
            return StandarizedErrorResponse(
                message='Failed to delete school Branch.',
                status_code=status.HTTP_404_NOT_FOUND)
        
        branch.isdeleted = True
        return StandarizedSuccessResponse(
            message=f'Successfully Deleted School Branch: "{branch.branch_name}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SchoolBranchSerializer,
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School Branch", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully updated school Branch.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to update school Branch.', StandarizedErrorResponseSerializer),
            404: openapi.Response('School Branch not found.', StandarizedErrorResponseSerializer),
        }
    )
    def put(self, request, pk, format=None):
        try:
            current_branch = self.queryset.objects.get(pk=pk)
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

