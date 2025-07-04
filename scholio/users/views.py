from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser,AllowAny,OR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.StandardResponse import standarizedErrorResponse, standarizedSuccessResponse
from utils.StandardResponse_serializers import (
    standarizedErrorResponseSerializer,
    standarizedSuccessResponseSerializer
    )
from schools.models import School
from .serializers import *
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

class BranchManagerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner)]
    
    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        responses={
            201: openapi.Response(
                'Successfully created Branch Manager.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to create Branch Manager.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            created_user = serializer.save(role = 'manager')
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Branch Manager "{created_user.email}".',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Branch manager.',
                status_code=status.HTTP_400_BAD_REQUEST)


class BranchManagerpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [OR(IsAdminUser(),IsSchoolOwner)]
        if self.request.method == 'DELETE':
            return [OR(IsAdminUser(),IsSchoolOwner)]
        if self.request.method == 'GET':
            return [AllowAny()]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Successfully Retrieved Branch manager.',
                standarizedSuccessResponseSerializer
                ),
            404: openapi.Response(
                'Failed to Retrieved Branch manager.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the Branch manager",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            manager = self.queryset.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve Branch Manager.',
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserCreateSerializer(manager)
        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available Branch Manager.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the Branch Manager",
                type=openapi.TYPE_INTEGER
                )
        ],
        responses={
            200: openapi.Response(
                'Successfully Deleted Branch Manager.',
                standarizedSuccessResponseSerializer
                ),
            404: openapi.Response(
                'Failed to delete Branch Manager.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def delete(self, request, pk):
        try:
            manager = self.queryset.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to delete Branch Manager.',
                status_code=status.HTTP_404_NOT_FOUND)

        manager.is_active = False
        manager.save()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted Branch Manager "{manager.email}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the Branch Manager",
                type=openapi.TYPE_INTEGER
                )
        ],
        responses={
            200: openapi.Response(
                'Successfully updated Branch Manager.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to update Branch Manager.',
                standarizedErrorResponseSerializer
                ),
            404: openapi.Response(
                'Branch Manager not found.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def put(self, request, pk, format=None):
        try:
            current_bm = self.queryset.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message="Branch Manager does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserCreateSerializer(current_bm, data=request.data)
        if serializer.is_valid():
            updated_bm = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Branch Manager "{updated_bm.email}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.email}".',
                status_code=status.HTTP_400_BAD_REQUEST)

 
class PrincipalAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner,IsBranchManager)]

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        responses={
            201: openapi.Response(
                'Successfully created Principal.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to create Principal.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            created_user = serializer.save(role='principal')
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Principal "{created_user.email}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Principal.',
                status_code=status.HTTP_400_BAD_REQUEST)


class PrincipalpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [OR(IsAdminUser(),IsSchoolOwner,IsBranchManager)]
        if self.request.method == 'DELETE':
            return [OR(IsAdminUser(),IsSchoolOwner,IsBranchManager)]
        if self.request.method == 'GET':
            return [AllowAny()]
        
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Successfully Retrieved Principal.',
                standarizedSuccessResponseSerializer
                ),
            404: openapi.Response(
                'Principal not found.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the Principal",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            principal = self.queryset.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Principal not found.',
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserCreateSerializer(principal)
        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available Principal.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the Principal",
                type=openapi.TYPE_INTEGER
                )
        ],
        responses={
            200: openapi.Response(
                'Successfully Deleted School.',
                standarizedSuccessResponseSerializer
                ),
            404: openapi.Response(
                'Principal not found.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def delete(self, request, pk):
        try:
            principal = self.queryset.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message='Principal not found.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        principal.is_active = False
        principal.save()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School "{principal.email}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER
                )
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
    def put(self, request, pk, format=None):
        try:
            current_principal = self.queryset.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message="Principal does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserCreateSerializer(current_principal, data=request.data)
        if serializer.is_valid():
            updated_principal = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Principal "{updated_principal.email}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update principal "{current_principal.email}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 

class OwnerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
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
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            created_user = serializer.save(role='owner')
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Owner "{created_user.email}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Owner.',
                status_code=status.HTTP_400_BAD_REQUEST)


class OwnerpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    # def get_queryset(self):
    #     return self.queryset.all()

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminUser()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        if self.request.method == 'GET':
            return [AllowAny()]
        
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
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            owner = self.queryset.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
            
        serializer = CustomUserCreateSerializer(owner)

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
                type=openapi.TYPE_INTEGER
                )
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
            school_owner = self.queryset.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school_owner.is_active = False
        school_owner.save()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School Owner"{school_owner.email}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER
                )
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
    def put(self, request, pk, format=None):
        try:
            current_owner = self.queryset.get(pk=pk)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message="Owner does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserCreateSerializer(current_owner, data=request.data)
        if serializer.is_valid():
            updated_owner = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Owner "{updated_owner.email}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Owner "{current_owner.email}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 