from django.urls import path
from . import views

urlpatterns = [
    path('branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManager' ),
    path('owner/', views.OwnerAPIview.as_view(), name='Owner' ),
    path('principal/', views.PrincipalAPIview.as_view(), name='Principal' ),

]
