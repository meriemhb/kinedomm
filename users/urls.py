from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:pk>/', views.user_profile, name='user_profile'),
    path('profile/<int:pk>/edit/', views.edit_user_profile, name='edit_user_profile'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
] 