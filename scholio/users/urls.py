from django.urls import path
from . import views

urlpatterns = [
    path('branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManager' ),
    path('branchmanager/<int:pk>', views.BranchManagerpkAPIview.as_view(), name='BranchManager' ),
    path('schoolowner/', views.OwnerAPIview.as_view(), name='Owner' ),
    path('schoolowner/<int:pk>', views.OwnerpkAPIview.as_view(), name='Owner' ),

]
