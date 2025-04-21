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
    path('kine/invite/', views.invite_patient, name='invite_patient'),
    path('conseils/', views.conseil_list, name='conseil_list'),
    path('conseils/create/', views.conseil_create, name='conseil_create'),
    path('conseils/<int:pk>/', views.conseil_detail, name='conseil_detail'),
    path('conseils/<int:pk>/update/', views.conseil_update, name='conseil_update'),
    path('conseils/<int:pk>/delete/', views.conseil_delete, name='conseil_delete'),
    path('treatment-requests/', views.treatment_requests_list, name='treatment_requests'),
    path('treatment-requests/create/', views.treatment_request_create, name='treatment_request_create'),
    path('treatment-requests/<int:pk>/', views.treatment_request_detail, name='treatment_request_detail'),
    path('treatment-invitations/', views.treatment_invitations, name='treatment_invitations'),
    path('treatment-invitations/<int:pk>/respond/', views.respond_to_invitation, name='respond_to_invitation'),
] 