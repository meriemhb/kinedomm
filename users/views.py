from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import Utilisateur, Patient, Kine, Vendeur, Settings
from django.views.generic import View
from appointments.models import Appointment
from django.db import models
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            if role == 'PATIENT':
                Patient.objects.create(utilisateur=user)
            elif role == 'KINE':
                Kine.objects.create(utilisateur=user)
            elif role == 'VENDEUR':
                Vendeur.objects.create(utilisateur=user)
            
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserRegistrationForm()
        role = request.GET.get('type', '')
        if role:
            form.fields['role'].initial = role.upper()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    
    if hasattr(user, 'patient_profile'):
        context['profile'] = user.patient_profile
    elif hasattr(user, 'kine_profile'):
        context['profile'] = user.kine_profile
    elif hasattr(user, 'vendeur_profile'):
        context['profile'] = user.vendeur_profile
    
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistiques générales
    total_users = Utilisateur.objects.count()
    total_appointments = Appointment.objects.count()
    total_kines = Kine.objects.count()
    total_patients = Patient.objects.count()
    
    # Rendez-vous du jour
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(
        date_heure__date=today
    ).count()
    
    # Derniers rendez-vous avec les informations des utilisateurs
    recent_appointments = Appointment.objects.select_related(
        'patient', 'kine'
    ).order_by('-date_heure')[:10]
    
    # Statistiques des rendez-vous par statut
    appointments_by_status = Appointment.objects.values(
        'statut'
    ).annotate(
        count=models.Count('id')
    )
    
    context = {
        'total_users': total_users,
        'total_appointments': total_appointments,
        'total_kines': total_kines,
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'recent_appointments': recent_appointments,
        'appointments_by_status': appointments_by_status,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = Utilisateur.objects.all()
    return render(request, 'admin/users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_appointments(request):
    appointments = Appointment.objects.all().order_by('-date_heure')
    return render(request, 'admin/appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    # Statistiques pour les rapports
    appointments_by_status = Appointment.objects.values('statut').annotate(count=models.Count('id'))
    
    # Rendez-vous par mois
    appointments_by_month = Appointment.objects.extra(
        select={'month': "strftime('%m/%Y', date_heure)"}
    ).values('month').annotate(count=models.Count('id')).order_by('month')
    
    # Statistiques du mois en cours
    current_month = timezone.now().strftime('%m/%Y')
    monthly_appointments = Appointment.objects.filter(
        date_heure__month=timezone.now().month,
        date_heure__year=timezone.now().year
    ).count()
    
    # Taux de complétion
    total_appointments = Appointment.objects.count()
    completed_appointments = Appointment.objects.filter(statut='COMPLETED').count()
    completion_rate = round((completed_appointments / total_appointments * 100) if total_appointments > 0 else 0, 1)
    
    # Nouveaux patients ce mois-ci
    new_patients = Patient.objects.filter(
        utilisateur__date_joined__month=timezone.now().month,
        utilisateur__date_joined__year=timezone.now().year
    ).count()
    
    # Taux d'annulation
    cancelled_appointments = Appointment.objects.filter(statut='CANCELLED').count()
    cancellation_rate = round((cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0, 1)
    
    # Statistiques mensuelles détaillées
    monthly_stats = []
    for i in range(6):  # Derniers 6 mois
        month = timezone.now() - timezone.timedelta(days=30*i)
        month_str = month.strftime('%m/%Y')
        
        month_appointments = Appointment.objects.filter(
            date_heure__month=month.month,
            date_heure__year=month.year
        )
        
        total = month_appointments.count()
        confirmed = month_appointments.filter(statut='CONFIRMED').count()
        completed = month_appointments.filter(statut='COMPLETED').count()
        cancelled = month_appointments.filter(statut='CANCELLED').count()
        
        completion_rate = round((completed / total * 100) if total > 0 else 0, 1)
        
        monthly_stats.append({
            'month': month_str,
            'total': total,
            'confirmed': confirmed,
            'completed': completed,
            'cancelled': cancelled,
            'completion_rate': completion_rate
        })
    
    context = {
        'appointments_by_status': appointments_by_status,
        'appointments_by_month': appointments_by_month,
        'monthly_appointments': monthly_appointments,
        'completion_rate': completion_rate,
        'new_patients': new_patients,
        'cancellation_rate': cancellation_rate,
        'monthly_stats': monthly_stats,
    }
    return render(request, 'admin/reports.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        site_name = request.POST.get('site_name')
        contact_email = request.POST.get('contact_email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        # Paramètres de notification
        email_notifications = request.POST.get('email_notifications') == 'on'
        sms_notifications = request.POST.get('sms_notifications') == 'on'
        appointment_reminders = request.POST.get('appointment_reminders') == 'on'
        
        # Paramètres de sécurité
        session_timeout = int(request.POST.get('session_timeout', 30))
        two_factor_auth = request.POST.get('two_factor_auth') == 'on'
        password_policy = request.POST.get('password_policy') == 'on'
        
        # Mettre à jour ou créer les paramètres
        settings, created = Settings.objects.get_or_create(pk=1)
        settings.site_name = site_name
        settings.contact_email = contact_email
        settings.phone_number = phone_number
        settings.address = address
        settings.email_notifications = email_notifications
        settings.sms_notifications = sms_notifications
        settings.appointment_reminders = appointment_reminders
        settings.session_timeout = session_timeout
        settings.two_factor_auth = two_factor_auth
        settings.password_policy = password_policy
        settings.save()
        
        messages.success(request, 'Les paramètres ont été mis à jour avec succès.')
        return redirect('admin_settings')
    
    # Charger les paramètres actuels
    try:
        settings = Settings.objects.get(pk=1)
    except Settings.DoesNotExist:
        settings = Settings.objects.create(pk=1)
    
    context = {
        'settings': settings
    }
    return render(request, 'users/admin_settings.html', context)

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(User, pk=pk, role='PATIENT')
    
    # Vérifier si l'utilisateur a le droit de voir ce profil
    if request.user.role != 'KINE' and request.user != patient:
        messages.error(request, "Vous n'avez pas accès à ce profil.")
        return redirect('home')
    
    # Récupérer les rendez-vous du patient avec le kiné actuel
    appointments = Appointment.objects.filter(
        patient=patient,
        kine=request.user
    ).order_by('-date_heure')
    
    context = {
        'patient': patient,
        'appointments': appointments
    }
    return render(request, 'users/patient_detail.html', context)

@login_required
@user_passes_test(is_admin)
def user_profile(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    context = {
        'user': user,
    }
    
    if hasattr(user, 'patient_profile'):
        context['profile'] = user.patient_profile
    elif hasattr(user, 'kine_profile'):
        context['profile'] = user.kine_profile
    elif hasattr(user, 'vendeur_profile'):
        context['profile'] = user.vendeur_profile
    
    return render(request, 'users/admin_profile.html', context)

@login_required
@user_passes_test(is_admin)
def edit_user_profile(request, pk):
    user = get_object_or_404(Utilisateur, pk=pk)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le profil a été mis à jour avec succès !')
            return redirect('users:user_profile', pk=user.pk)
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/admin_edit_profile.html', {'form': form, 'user': user})
