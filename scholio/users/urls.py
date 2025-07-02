from django.urls import path
from . import views

urlpatterns = [
    path('branchmanager/', views.BranchManagerAPIview.as_view(), name='BranchManager' ),
    path('branchmanager/<int:pk>', views.BranchManagerpkAPIview.as_view(), name='BranchManager' ),
    path('owner/', views.OwnerAPIview.as_view(), name='Owner' ),
    path('owner/<int:pk>', views.OwnerpkAPIview.as_view(), name='Owner' ),
    path('principal/', views.PrincipalAPIview.as_view(), name='Principal' ),
    path('principal/<int:pk>', views.PrincipalpkAPIview.as_view(), name='Principal' ),

]
