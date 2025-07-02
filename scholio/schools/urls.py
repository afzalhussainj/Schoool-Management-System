from django.urls import path

# from django.urls import include
from . import views


urlpatterns = [
    path('school/', views.SchoolAPIView.as_view(), name='School' ),
    path('school/<int:pk>', views.SchoolpkAPIView.as_view(), name='School' ),
    path('branch/', views.SchoolBranchAPIview.as_view(), name='SchoolBranch' ),
    path('branch/<int:pk>', views.SchoolBranchpkAPIview.as_view(), name='SchoolBranch' ),
]
