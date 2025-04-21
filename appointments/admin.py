from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'kine', 'date_heure', 'statut', 'duree')
    list_filter = ('statut', 'date_heure')
    search_fields = ('patient__username', 'kine__username', 'notes')
    date_hierarchy = 'date_heure'
