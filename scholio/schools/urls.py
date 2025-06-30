from django.urls import path
from . import views

urlpatterns = [
    path('create/school/', views.SchoolAPIview.as_view(), name='SchoolCreation' ),
    path('update/school/<int:pk>', views.SchoolAPIview.as_view(), name='SchoolUpdation' ),
    path('create/branch/', views.SchoolBranchAPIview.as_view(), name='SchoolBranchCreation' ),
    path('update/branch/<int:pk>', views.SchoolBranchAPIview.as_view(), name='SchoolBranchUpdation' ),
]