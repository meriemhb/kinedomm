"""
URL configuration for kine_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from users.views import (
    logout_view, admin_dashboard, admin_users, 
    admin_appointments, admin_reports, admin_settings, 
    register
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('appointments/', include('appointments.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    
    # URLs du tableau de bord administrateur
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', admin_users, name='admin_users'),
    path('dashboard/appointments/', admin_appointments, name='admin_appointments'),
    path('dashboard/reports/', admin_reports, name='admin_reports'),
    path('dashboard/settings/', admin_settings, name='admin_settings'),
    
    # Pages statiques
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('legal/', TemplateView.as_view(template_name='legal.html'), name='legal'),
]
