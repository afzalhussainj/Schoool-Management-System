from django.urls import path
from . import views

urlpatterns = [
    path('create/school/', views.SchoolAPIview.as_view(), name='SchoolCreation' ),
    path('update/school/<int:pk>', views.SchoolAPIview.as_view(), name='SchoolUpdation' ),
]