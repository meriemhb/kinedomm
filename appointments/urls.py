from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='list'),
    path('create/', views.appointment_create, name='create'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:pk>/update/', views.appointment_update, name='update'),
    path('<int:pk>/delete/', views.appointment_delete, name='delete'),
    path('kine/', views.kine_appointment_list, name='kine_list'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('kine/patients/', views.kine_patient_list, name='kine_patients'),
    path('kine/availabilities/', views.availability_list, name='availability_list'),
    path('kine/availabilities/create/', views.availability_create, name='availability_create'),
    path('kine/availabilities/<int:pk>/delete/', views.availability_delete, name='availability_delete'),
    path('statistics/', views.statistics, name='statistics'),
] 