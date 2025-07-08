from django.urls import path
from . import views

urlpatterns = [
    path('branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManager' ),
    path('branchmanager/<uuid:uuid>', views.BranchManageruuidAPIview.as_view(), name='BranchManager' ),
    path('schoolowner/', views.OwnerAPIview.as_view(), name='Owner' ),
    path('schoolowner/<uuid:uuid>', views.OwneruuidAPIview.as_view(), name='Owner' ),

]
