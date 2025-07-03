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
from .models import Principal
from .serializers import *
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

class BranchManagerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = BranchManager.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner)]
    
    @swagger_auto_schema(
        request_body=BranchManagerSerializer,
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
        serializer = BranchManagerSerializer(data=request.data)
        if serializer.is_valid():
            created_bm = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Branch Manager "{created_bm.name}".',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Branch manager.',
                status_code=status.HTTP_400_BAD_REQUEST)


class BranchManagerpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = BranchManager.objects.filter(isdeleted=False)

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
        },
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_QUERY,
                description="Primary Key of the Branch manager",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            manager = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = BranchManagerSerializer(manager)
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
            manager = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to delete Branch Manager.',
                status_code=status.HTTP_404_NOT_FOUND)

        manager.isdeleted = True
        return standarizedSuccessResponse(
            message=f'Successfully Deleted Branch Manager "{manager.name}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BranchManagerSerializer,
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
            current_bm = self.queryset.objects.get(pk=pk)
        except BranchManager.DoesNotExist:
            return standarizedErrorResponse(
                message="Branch Manager does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = BranchManagerSerializer(current_bm, data=request.data)
        if serializer.is_valid():
            updated_bm = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Branch Manager "{updated_bm.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)

 
class PrincipalAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = Principal.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner,IsBranchManager)]

    @swagger_auto_schema(
        request_body=PrincipalSerializer,
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
        serializer = PrincipalSerializer(data=request.data)
        if serializer.is_valid():
            created_principal = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Principal "{created_principal.name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Principal.',
                status_code=status.HTTP_400_BAD_REQUEST)


class PrincipalpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = Principal.objects.filter(isdeleted=False)

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
            principal = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = PrincipalSerializer(principal)
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
            principal = self.queryset.objects.get(pk=pk)
        except Principal.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        principal.isdeleted = True
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School "{principal.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=PrincipalSerializer,
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
            current_principal = self.queryset.objects.get(pk=pk)
        except Principal.DoesNotExist:
            return standarizedErrorResponse(
                message="Principal does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = PrincipalSerializer(current_principal, data=request.data)
        if serializer.is_valid():
            updated_principal = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Principal "{updated_principal.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update principal "{current_principal.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 

class OwnerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = SchoolOwner.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
    @swagger_auto_schema(
        request_body=SchoolOwnerSerializer,
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
        serializer = SchoolOwnerSerializer(data=request.data)
        if serializer.is_valid():
            created_owner = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Owner "{created_owner.name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Owner.',
                status_code=status.HTTP_400_BAD_REQUEST)

class OwnerpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = SchoolOwner.objects.filter(isdeleted=False)

    def get_queryset(self):
        return self.queryset.all()

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
                openapi.IN_QUERY,
                description="Primary Key of the School",
                type=openapi.TYPE_INTEGER,
                # required=False
                )
        ],
    )
    def get(self, request, pk):
        try:
            owner = self.queryset.objects.get(pk=pk)
        except:
            return standarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
            
        serializer = SchoolOwnerSerializer(owner)

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
            school_owner = self.queryset.objects.get(pk=pk)
        except SchoolOwner.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school_owner.isdeleted = True
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School "{school_owner.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=SchoolOwnerSerializer,
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
            current_owner = self.queryset.objects.get(pk=pk)
        except SchoolOwner.DoesNotExist:
            return standarizedErrorResponse(
                message="Owner does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolOwnerSerializer(current_owner, data=request.data)
        if serializer.is_valid():
            updated_owner = serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Owner "{updated_owner.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Owner "{current_owner.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 