from rest_framework import permissions
from .models import *

class IsSchoolOwner(permissions.BasePermission):
    """
    Check for if the user is the owner of School.
    """

    def has_permission(self, request, view):
        return bool(
            request.user 
            and 
            request.user.is_authenticated
            and 
            request.use.role == 'manager'
            )
    
class IsBranchManager(permissions.BasePermission):
    """
    Check for if the user is Branch Manager
    """

    def has_permission(self, request, view):
        return (
            request.user 
            and 
            request.user.is_authenticated
            and 
            request.use.role == 'manager'
            )