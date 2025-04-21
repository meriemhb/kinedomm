from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import Utilisateur
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Availability
from .forms import AppointmentForm, AvailabilityForm

def is_admin(user):
    return user.is_staff

@login_required
def appointment_list(request):
    if request.user.role == 'PATIENT':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.role == 'KINE':
        appointments = Appointment.objects.filter(kine=request.user)
    else:
        appointments = []
    
    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/list.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.role == 'PATIENT':
                appointment.patient = request.user
            elif request.user.role == 'KINE':
                appointment.kine = request.user
            appointment.save()
            messages.success(request, 'Rendez-vous créé avec succès.')
            return redirect('appointments:list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    return render(request, 'appointments/detail.html', {'appointment': appointment})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rendez-vous mis à jour avec succès.')
            return redirect('appointments:detail', pk=pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/form.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user not in [appointment.patient, appointment.kine]:
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('appointments:list')
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Rendez-vous supprimé avec succès.')
        return redirect('appointments:list')
    
    return render(request, 'appointments/delete.html', {'appointment': appointment})

@login_required
def kine_appointment_list(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    statut = request.GET.get('statut')
    appointments = Appointment.objects.filter(kine=request.user)
    
    if statut:
        appointments = appointments.filter(statut=statut)
    
    context = {
        'appointments': appointments,
        'current_status': statut
    }
    return render(request, 'appointments/kine_list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistiques générales
    total_users = Utilisateur.objects.count()
    total_kines = Utilisateur.objects.filter(role='KINE').count()
    total_patients = Utilisateur.objects.filter(role='PATIENT').count()
    
    # Rendez-vous du jour
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(
        date_heure__date=today
    ).count()
    
    # Derniers rendez-vous
    recent_appointments = Appointment.objects.select_related(
        'patient', 'kine'
    ).order_by('-date_heure')[:10]
    
    context = {
        'total_users': total_users,
        'total_kines': total_kines,
        'total_patients': total_patients,
        'today_appointments': today_appointments,
        'recent_appointments': recent_appointments,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
def kine_patient_list(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    # Récupérer tous les patients qui ont eu au moins un rendez-vous avec ce kiné
    patients = Utilisateur.objects.filter(
        role='PATIENT',
        appointments_as_patient__kine=request.user
    ).distinct()
    
    context = {
        'patients': patients
    }
    return render(request, 'appointments/kine_patient_list.html', context)

@login_required
def availability_list(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    availabilities = Availability.objects.filter(
        kine=request.user,
        jour__gte=timezone.now().date()
    ).order_by('jour', 'heure_debut')
    
    context = {
        'availabilities': availabilities
    }
    return render(request, 'appointments/availability_list.html', context)

@login_required
def availability_create(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.kine = request.user
            availability.save()
            messages.success(request, "Disponibilité ajoutée avec succès.")
            return redirect('appointments:availability_list')
    else:
        form = AvailabilityForm()
    
    context = {
        'form': form
    }
    return render(request, 'appointments/availability_form.html', context)

@login_required
def availability_delete(request, pk):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    availability = get_object_or_404(Availability, pk=pk, kine=request.user)
    
    if request.method == 'POST':
        availability.delete()
        messages.success(request, "Disponibilité supprimée avec succès.")
        return redirect('appointments:availability_list')
    
    context = {
        'availability': availability
    }
    return render(request, 'appointments/availability_confirm_delete.html', context)

@login_required
def statistics(request):
    if request.user.role != 'KINE':
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('home')
    
    # Statistiques des rendez-vous
    total_appointments = Appointment.objects.filter(kine=request.user).count()
    confirmed_appointments = Appointment.objects.filter(kine=request.user, statut='CONFIRME').count()
    cancelled_appointments = Appointment.objects.filter(kine=request.user, statut='ANNULE').count()
    completed_appointments = Appointment.objects.filter(kine=request.user, statut='TERMINE').count()
    
    # Statistiques des patients
    total_patients = Utilisateur.objects.filter(
        role='PATIENT',
        appointments_as_patient__kine=request.user
    ).distinct().count()
    
    context = {
        'total_appointments': total_appointments,
        'confirmed_appointments': confirmed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'completed_appointments': completed_appointments,
        'total_patients': total_patients,
    }
    
    return render(request, 'appointments/statistics.html', context)
