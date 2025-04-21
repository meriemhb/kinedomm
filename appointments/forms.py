from django import forms
from .models import Appointment, Availability
from users.models import Utilisateur
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['kine', 'date_heure', 'duree', 'notes']
        widgets = {
            'date_heure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duree': forms.NumberInput(attrs={'min': '15', 'max': '120', 'step': '15'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kine'].queryset = Utilisateur.objects.filter(role='KINE')
        self.fields['kine'].label = 'Kinésithérapeute'
        self.fields['date_heure'].label = 'Date et heure'
        self.fields['duree'].label = 'Durée (minutes)'
        self.fields['notes'].label = 'Notes'

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['jour', 'heure_debut', 'heure_fin', 'duree_rdv']
        widgets = {
            'jour': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'duree_rdv': forms.NumberInput(attrs={'min': 15, 'max': 120, 'step': 15}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        jour = cleaned_data.get('jour')
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        
        if jour and heure_debut and heure_fin:
            if jour < timezone.now().date():
                raise forms.ValidationError("La date ne peut pas être dans le passé.")
            
            if heure_fin <= heure_debut:
                raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")
        
        return cleaned_data 