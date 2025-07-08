from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser,AllowAny,OR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
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
from django.utils import timezone

# Create your views here.

class BranchManagerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner)]
    
    @swagger_auto_schema(
        tags=['User Creations'],
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


class BranchManageruuidAPIview(APIView):
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
        tags=['User Details'],
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
                'uuid',
                openapi.IN_PATH,
                description="Primary Key of the Branch manager",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, uuid):
        try:
            manager = self.queryset.get(uuid=uuid)
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
        tags=['User Deletions'],
        manual_parameters=[
            openapi.Parameter(
                'uuid',
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
    def delete(self, request, uuid):
        try:
            manager = self.queryset.get(uuid=uuid)
        except:
            return standarizedErrorResponse(
                message='Failed to delete Branch Manager.',
                status_code=status.HTTP_404_NOT_FOUND)

        manager.is_active = False
        manager.deleted_at = timezone.now()
        manager.deleted_by = self.request.user
        manager.save()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted Branch Manager "{manager.email}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['User Updates'],
        request_body=CustomUserCreateSerializer,
        manual_parameters=[
            openapi.Parameter(
                'uuid',
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
    def put(self, request, uuid, format=None):
        try:
            current_bm = self.queryset.get(uuid=uuid)
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

 
class OwnerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.filter(is_active=False)
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
    @swagger_auto_schema(
        tags=['User Creations'],
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


class OwneruuidAPIview(APIView):
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
        tags=['User Details'],
        responses={
            200: openapi.Response(
                'Successfully Retrieved School.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'uuid',
                openapi.IN_PATH,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, uuid):
        try:
            owner = self.queryset.get(uuid=uuid)
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
        tags=['User Deletions'],
        manual_parameters=[
            openapi.Parameter(
                'uuid',
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
    def delete(self, request, uuid):
        try:
            school_owner = self.queryset.get(uuid=uuid)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school_owner.is_active = False
        school_owner.deleted_at = timezone.now()
        school_owner.deleted_by = self.request.user
        school_owner.save()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School Owner"{school_owner.email}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        tags=['User Updates'],
        request_body=CustomUserCreateSerializer,
        manual_parameters=[
            openapi.Parameter(
                'uuid',
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
    def put(self, request, uuid, format=None):
        try:
            current_owner = self.queryset.get(uuid=uuid)
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
 

class LoginAPIview(APIView):
    permission_classes=[AllowAny]

    @swagger_auto_schema(
        tags=['Login'],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                'Successfully logged in.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to log in.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user:
                refresh = RefreshToken.for_user(user=user)
                access = refresh.access_token
                user_data = UserDetailsSerializer(user).data
                return standarizedSuccessResponse(
                    message='User Successfully logined.',
                    data={
                        'user':user_data,
                        'user_email':user.email,
                        'access':str(access),
                        'refresh':str(refresh)
                    },
                    status_code=status.HTTP_200_OK
                )
        else:
            return standarizedErrorResponse(
                message=serializer.error_messages,
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

