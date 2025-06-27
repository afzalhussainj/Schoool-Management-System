from rest_framework import permissions
from .models import *

class IsSchoolOwner(permissions.BasePermission):
    """
    Check for if the user is the owner of School.
    """

    def has_permission(self, request, view):
        return SchoolOwner.objects.filter(request.user).exists()
    
class IsBranchManager(permissions.BasePermission):
    """
    Check for if the user is Branch Manager
    """

    def has_permission(self, request, view):
        return BranchManager.objects.filter(request.user).exists()