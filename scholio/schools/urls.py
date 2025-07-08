from django.urls import path

# from django.urls import include
from . import views


urlpatterns = [
    path('school/', views.SchoolAPIView.as_view(), name='School' ),
    path('school/<uuid:uuid>', views.SchooluuidAPIView.as_view(), name='School' ),
    path('branch/', views.SchoolBranchAPIview.as_view(), name='SchoolBranch' ),
    path('branch/<uuid:uuid>', views.SchoolBranchuuidAPIview.as_view(), name='SchoolBranch' ),
]
