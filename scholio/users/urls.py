from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.CustomUserAPIview.as_view(), name='user' ),
    path('branchmanager/<uuid:uuid>', views.BranchManageruuidAPIview.as_view(), name='BranchManager' ),
    path('schoolowner/<uuid:uuid>', views.OwneruuidAPIview.as_view(), name='Owner' ),

]
