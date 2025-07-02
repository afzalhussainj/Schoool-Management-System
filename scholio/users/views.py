from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser,AllowAny,OR
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.StandardResponse import StandarizedErrorResponse, StandarizedSuccessResponse
from utils.StandardResponse_serializers import StandarizedErrorResponseSerializer,StandarizedSuccessResponseSerializer
from schools.models import School
from .models import Principal
from .serializers import *
from .permissions import IsBranchManager, IsSchoolOwner

# Create your views here.

class BranchManagerAPIview(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner)]
    
    @swagger_auto_schema(
        request_body=BranchManagerSerializer,
        responses={
            201: openapi.Response('Successfully created School.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to create School.', StandarizedErrorResponseSerializer),
        }
    )
    def post(self, request):
        serializer = BranchManagerSerializer(data=request.data)
        if serializer.is_valid():
            created_bm = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Branch Manager "{created_bm.name}".',
                status_code=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
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
            200: openapi.Response('Successfully Retrieved Branch manager.',StandarizedSuccessResponseSerializer),
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
            manager = BranchManager.objects.get(pk=pk)
        except:
            return StandarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
        serialized_data = BranchManagerSerializer(manager)
        return StandarizedSuccessResponse(
            data=serialized_data.data,
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
            manager = BranchManager.objects.get(pk=pk)
        except:
            return StandarizedErrorResponse(
                message='Failed to delete Branch Manager.',
                status_code=status.HTTP_404_NOT_FOUND)

        manager.isdeleted = True
        return StandarizedSuccessResponse(
            message=f'Successfully Deleted Branch Manager "{manager.name}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BranchManagerSerializer,
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully updated school.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to update school.', StandarizedErrorResponseSerializer),
            404: openapi.Response('School not found.', StandarizedErrorResponseSerializer),
        }
    )
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
                message=f'Successfully updated Branch Manager "{updated_bm.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)

 
class PrincipalAPIview(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [OR(IsAdminUser(),IsSchoolOwner,IsBranchManager)]

    @swagger_auto_schema(
        request_body=PrincipalSerializer,
        responses={
            201: openapi.Response('Successfully created School.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to create School.', StandarizedErrorResponseSerializer),
        }
    )
    def post(self, request):
        serializer = PrincipalSerializer(data=request.data)
        if serializer.is_valid():
            created_principal = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Principal "{created_principal.name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
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
            principal = Principal.objects.get(pk=pk)
        except:
            return StandarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
        serialized_data = PrincipalSerializer(principal)
        return StandarizedSuccessResponse(
            data=serialized_data.data,
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
            principal = Principal.objects.get(pk=pk)
        except Principal.DoesNotExist:
            return StandarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        principal.isdeleted = True
        return StandarizedSuccessResponse(
            message=f'Successfully Deleted School "{principal.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=PrincipalSerializer,
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully updated school.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to update school.', StandarizedErrorResponseSerializer),
            404: openapi.Response('School not found.', StandarizedErrorResponseSerializer),
        }
    )
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
                message=f'Successfully updated Principal "{updated_principal.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update principal "{current_principal.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 

class OwnerAPIview(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
    @swagger_auto_schema(
        request_body=SchoolOwnerSerializer,
        responses={
            201: openapi.Response('Successfully created School.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to create School.', StandarizedErrorResponseSerializer),
        }
    )
    def post(self, request):
        serializer = SchoolOwnerSerializer(data=request.data)
        if serializer.is_valid():
            created_owner = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully created Owner "{created_owner.name}"',
                status_code=status.HTTP_201_CREATED)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message='Failed to create Owner.',
                status_code=status.HTTP_400_BAD_REQUEST)

class OwnerpkAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    quaryset = SchoolOwner.objects.filter(isdeleted=False)

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminUser()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        if self.request.method == 'GET':
            return [AllowAny()]
        
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
            owner = SchoolOwner.objects.get(pk=pk)
        except:
            return StandarizedErrorResponse(
                message='Failed to retrieve School.',
                status_code=status.HTTP_404_NOT_FOUND)
            
        serialized_data = SchoolOwnerSerializer(owner)

        return StandarizedSuccessResponse(
            data=serialized_data.data,
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
            school_owner = School.objects.get(pk=pk)
        except SchoolOwner.DoesNotExist:
            return StandarizedErrorResponse(
                message='Failed to delete school.',
                status_code=status.HTTP_404_NOT_FOUND
            )

        school_owner.isdeleted = True
        return StandarizedSuccessResponse(
            message=f'Successfully Deleted School "{school_owner.name}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=SchoolOwnerSerializer,
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary Key of the School", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response('Successfully updated school.', StandarizedSuccessResponseSerializer),
            400: openapi.Response('Failed to update school.', StandarizedErrorResponseSerializer),
            404: openapi.Response('School not found.', StandarizedErrorResponseSerializer),
        }
    )
    def put(self, request, pk, format=None):
        try:
            current_owner = SchoolOwner.objects.get(pk=pk)
        except SchoolOwner.DoesNotExist:
            return StandarizedErrorResponse(
                message="Owner does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = SchoolOwnerSerializer(current_owner, data=request.data)
        if serializer.is_valid():
            updated_owner = serializer.save()
            return StandarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Owner "{updated_owner.name}"',
                status_code=status.HTTP_200_OK)
        else:
            return StandarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Owner "{current_owner.name}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 