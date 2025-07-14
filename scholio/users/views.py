from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    OR,
    IsAuthenticated
    )
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from utils.StandardResponse import standarizedErrorResponse, standarizedSuccessResponse
from utils.StandardResponse_serializers import (
    standarizedErrorResponseSerializer,
    standarizedSuccessResponseSerializer
    )
from .serializers import *
from utils.permissions import *
from utils.enumerations import RoleChoices

# Create your views here.

class BranchManagerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSchoolOwner()]
    
    @swagger_auto_schema(
        tags=['User'],
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
        serializer = CustomUserCreateSerializer(data=request.data,context={'created_by':request.user})
        if serializer.is_valid():
            created_user = serializer.save(
                role=RoleChoices.manager.value
                )
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
    queryset = CustomUserModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminUser()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        if self.request.method == 'GET':
            return [AllowAny()]
    
    @swagger_auto_schema(
        tags=['User'],
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
        tags=['User'],
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

        manager.delete()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted Branch Manager "{manager.email}"',
            status_code=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['User'],
        request_body=CustomUserUpdateSerializer,
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
    def patch(self, request, uuid):
        try:
            current_bm = self.queryset.get(uuid=uuid)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message="Branch Manager does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserUpdateSerializer(
            current_bm,
            data=request.data,
            partial=True,
            context={'updated_by':request.user}
            )
        if serializer.is_valid():
            serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated Branch Manager "{serializer.instance.email}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update Branch Manager "{current_bm.email}".',
                status_code=status.HTTP_400_BAD_REQUEST)

 
class OwnerAPIview(APIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomUserModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        
    @swagger_auto_schema(
        tags=['User'],
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
        serializer = CustomUserCreateSerializer(data=request.data,context={'created_by':request.user})
        if serializer.is_valid():
            created_user = serializer.save(role=RoleChoices.owner.value)
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
    queryset = CustomUserModel.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAdminUser()]
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        if self.request.method == 'GET':
            return [AllowAny()]
        
    @swagger_auto_schema(
        tags=['User'],
        responses={
            200: openapi.Response(
                'Successfully Retrieved School.',
                standarizedSuccessResponseSerializer
                ),
        },
    )
    def get(self, request, uuid):
        try:
            owner = self.queryset.get(uuid=uuid)
        except:
            return standarizedErrorResponse(
                message='School Owner not found.',
                status_code=status.HTTP_404_NOT_FOUND)
            
        serializer = CustomUserCreateSerializer(owner)

        return standarizedSuccessResponse(
            data=serializer.data,
            message=f'Successfully retrieved Available School.',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        tags=['User'],
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

        school_owner.delete()
        return standarizedSuccessResponse(
            message=f'Successfully Deleted School Owner"{school_owner.email}"',
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        tags=['User'],
        request_body=CustomUserUpdateSerializer,
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
    def patch(self, request, uuid):
        try:
            current_owner = self.queryset.get(uuid=uuid)
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message="School owner does'nt exist.",
                status_code=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserUpdateSerializer(
            current_owner,
            data=request.data,
            partial=True,
            context={'updated_by':request.user}
            )
        if serializer.is_valid():
            serializer.save()
            return standarizedSuccessResponse(
                data=serializer.data,
                message=f'Successfully updated School Owner "{serializer.instance.email}"',
                status_code=status.HTTP_200_OK)
        else:
            return standarizedErrorResponse(
                details=serializer.errors,
                message=f'Failed to update School Owner "{current_owner.email}".',
                status_code=status.HTTP_400_BAD_REQUEST)
 

class ListUsersAPIview(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[JWTAuthentication]
    queryset = CustomUserModel.objects.all()

    @swagger_auto_schema(
        tags=['User'],
        responses={
            200: openapi.Response(
                'Retrieved users.',
                standarizedSuccessResponseSerializer
                ),
        },
        manual_parameters=[
            openapi.Parameter(
                'role',
                openapi.IN_QUERY,
                description='Role of the user: ' + ', '.join([f"{role.name}({role.value})" for role in RoleChoices]),
                type= openapi.TYPE_INTEGER,
                enum=[i.value for i in RoleChoices],
                required=False
            )
        ]
    )
    def get(self, request):
        role = request.query_params.get('role',None)
        users = self.queryset.all()
        if role:
            users = users.filter(role=role)
        serializer = CustomUserDetailsSerializer(users,many=True)
        return standarizedSuccessResponse(
            message='Successfully Reyrieved users.',
                    data={
                        'users':serializer.data
                    },
                    status_code=status.HTTP_200_OK
                    )


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
                user_data = CustomUserDetailsSerializer(user).data
                user.last_login = timezone.now()
                user.save()
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
                message='Login Failed',
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        

class PasswordChangeAPIview(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    @swagger_auto_schema(
        tags=['Password'],
        request_body=PasswordChangeSerializer,
        responses={
            200: openapi.Response(
                'Successfully Changed password.',
                standarizedSuccessResponseSerializer
                ),
            400: openapi.Response(
                'Failed to Changed password.',
                standarizedErrorResponseSerializer
                ),
            404: openapi.Response(
                'User not found.',
                standarizedErrorResponseSerializer
                ),
            403: openapi.Response(
                'Unauthenticated request.',
                standarizedErrorResponseSerializer
                ),
        }
    )
    def patch(self, request, uuid):
        try:
            target_user = CustomUserModel.objects.get(uuid=uuid)
            if (
                request.user.role == RoleChoices.admin.value
                or
                request.user == target_user
                ):
                serializer = PasswordChangeSerializer(data=request.data)
                if serializer.is_valid():
                    old_password = serializer.validated_data.get('old_password')
                    new_password = serializer.validated_data.get('new_password')
                    if target_user.check_password(old_password):
                        target_user.set_password(new_password)
                        target_user.save()
                        return standarizedSuccessResponse(
                             message='Successfully changed password.',
                            data={},
                            status_code=status.HTTP_200_OK
                            )
                    else:
                        return standarizedErrorResponse(
                            message='Failed to change password',
                            details={'incorrect password':'old password is not correct'},
                            status_code=status.HTTP_400_BAD_REQUEST
                            )
                else:
                    return standarizedErrorResponse(
                        message='Failed to change password.',
                        details=serializer.errors,
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return standarizedErrorResponse(
                    message='Unable to change password.',
                    details={'unauthenticated_request':'Unable to authenticate request'},
                    status_code=status.HTTP_403_FORBIDDEN
                    )
        except CustomUserModel.DoesNotExist:
            return standarizedErrorResponse(
                message='Failed to change password',
                details={'user_not_found':'User does not exists.'},
                status_code=status.HTTP_404_NOT_FOUND
                )

