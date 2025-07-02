from django.urls import path

# from django.urls import include
from . import views


urlpatterns = [
    path('school/', views.SchoolAPIView.as_view(), name='School' ),
    # path('school/<int:pk>', views.SchoolAPIView.as_view(), name='School' ),
]
