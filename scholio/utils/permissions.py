from rest_framework.permissions import BasePermission
from users.models import RoleChoices

class IsSchoolOwner(BasePermission):
    """
    Check for if the user is the owner of School.
    """

    def has_permission(self, request, view):
        print("User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        print("Role:", request.user.role)
        print("Is Staff:", request.user.is_staff)

        return (
            request.user 
            and 
            request.user.is_authenticated
            and 
            request.user.role == str(RoleChoices.owner.value)
        )


class IsBranchManager(BasePermission):
    """
    Check for if the user is Branch Manager
    """

    def has_permission(self, request, view):
        return (
            request.user 
            and 
            request.user.is_authenticated
            and 
            request.user.role == RoleChoices.manager.value
            )
    
    
class IsAdminOrSchoolOwner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or
                request.user.role == str(RoleChoices.owner.value)
            )
        )
    

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff 
                or 
                request.user.role == RoleChoices.manager.value
            )
        )