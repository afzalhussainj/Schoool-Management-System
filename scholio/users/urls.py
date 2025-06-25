from django.urls import path
import views

urlpatterns = [
    path('create/school/', views.SchoolCreateiew.as_view(), name='SchoolCreation' ),
    path('create/princile/', views.PrincipalCreateiew.as_view(), name='PrincipleCreation' )
]