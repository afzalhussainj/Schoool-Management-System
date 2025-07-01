from django.urls import path
from . import views

urlpatterns = [
    #branch manager
    path('create/branchmanager/', views.BranchManagerCreateAPIview.as_view(), name='BranchManagerCreation' ),
    path('all/managers/', views.BranchManagerRetrieveAllAPIview.as_view(), name='ManagerRetrivalAll' ),
    path('all/managers-specific/<int:pk>', views.BranchManagerRetrieveAllSpecificAPIview.as_view(), name='BranchSpecificManagerRetrivalAll' ),
    path('manager/<int:pk>', views.BranchManagerRetrieveSpecificAPIview.as_view(), name='ManagerRetrivalSpecific' ),
    path('update/branchmanager/<int:pk>', views.BranchManagerUpdateAPIview.as_view(), name='BranchManagerUpdation' ),
    # path('del/branch/<int:pk>', views.SchoolBranchDeleteAPIview.as_view(), name='SchoolBranchDelete' ),

    #principal
    path('create/princile/', views.PrincipalCreateAPIview.as_view(), name='PrincipalCreation' ),
    path('update/princile/<int:pk>', views.PrincipalUpdateAPIview.as_view(), name='PrincipalUpdation' ),

    #owner
    path('create/owner/', views.OwnerCreateAPIview.as_view(), name='OwnerCreation' ),
    path('update/owner/<int:pk>', views.OwnerUpdateAPIview.as_view(), name='OwnerUpdation' ),
    # path('create/princile/', views.PrincipalAPIview.as_view(), name='PrincipalCreation' ),
    # path('update/princile/<int:pk>', views.PrincipalAPIview.as_view(), name='PrincipalUpdation' ),
    # path('create/branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManagerCreation' ),
    # path('update/branchmanager/<int:pk>', views.BranchManagerAPIview.as_view(), name='BranchManagerUpdation' ),
    # path('create/owner/', views.OwnerAPIview.as_view(), name='OwnerCreation' ),
    # path('update/owner/<int:pk>', views.OwnerAPIview.as_view(), name='OwnerUpdation' ),
]
