from django.urls import path

# from django.urls import include
from . import views


urlpatterns = [
    # schools
    path('', views.SchoolAPIView.as_view(), name='School' ),
    # path('all/schools/', views.SchoolRetrieveAllAPIview.as_view(), name='SchoolRetrivalAll' ),
    # path('school/<int:pk>', views.SchoolRetrieveSpecificAPIview.as_view(), name='SchoolRetrivalSpecific' ),
    # path('update/school/<int:pk>', views.SchoolUpdateAPIview.as_view(), name='SchoolUpdation' ),
    # path('del/school/<int:pk>', views.SchoolDeleteAPIview.as_view(), name='SchoolDelete' ),
    
    #branches
    path('create/branch/', views.SchoolBranchCreateAPIview.as_view(), name='SchoolBranchCreation' ),
    path('all/branches/', views.SchoolBranchRetrieveAllAPIview.as_view(), name='SchoolBranchRetrivalAll' ),
    path('all/branches-specific/<int:pk>', views.SchoolBranchRetrieveAllSpecificAPIview.as_view(), name='SchoolSpecificBranchRetrivalAll' ),
    path('branch/<int:pk>', views.SchoolBranchRetrieveSpecificAPIview.as_view(), name='SchoolBranchRetrivalAll' ),
    path('update/branch/<int:pk>', views.SchoolBranchUpdateAPIview.as_view(), name='SchoolBranchUpdation' ),
    path('del/branch/<int:pk>', views.SchoolBranchDeleteAPIview.as_view(), name='SchoolBranchDelete' ),
    # path('create/school/', views.SchoolAPIview.as_view(), name='SchoolCreation' ),
    # path('update/school/<int:pk>', views.SchoolAPIview.as_view(), name='SchoolUpdation' ),
    # path('create/branch/', views.SchoolBranchAPIview.as_view(), name='SchoolBranchCreation' ),
    # path('update/branch/<int:pk>', views.SchoolBranchAPIview.as_view(), name='SchoolBranchUpdation' ),
]
