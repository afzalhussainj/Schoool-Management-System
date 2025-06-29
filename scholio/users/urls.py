from django.urls import path
from . import views

urlpatterns = [
    path('create/princile/', views.PrincipalAPIview.as_view(), name='PrincipalCreation' ),
    path('update/princile/<int:pk>', views.PrincipalAPIview.as_view(), name='PrincipalUpdation' ),
    path('create/branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManagerCreation' ),
    path('update/branchmanager/<int:pk>', views.BranchManagerAPIview.as_view(), name='BranchManagerUpdation' ),
    path('create/owner/', views.OwnerAPIview.as_view(), name='OwnerCreation' ),
    path('update/owner/<int:pk>', views.OwnerAPIview.as_view(), name='OwnerUpdation' ),
]
