from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListUsersAPIview.as_view(), name='users' ),
    path('branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManagers' ),
    path('branchmanager/<uuid:uuid>', views.BranchManageruuidAPIview.as_view(), name='BranchManager' ),
    path('schoolowner/', views.OwnerAPIview.as_view(), name='Owners' ),
    path('schoolowner/<uuid:uuid>', views.OwneruuidAPIview.as_view(), name='Owner' ),

]
