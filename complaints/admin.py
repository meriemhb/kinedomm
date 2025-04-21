from django.contrib import admin
from .models import Reclamation

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('get_patient', 'type_destinataire', 'get_destinataire', 'date', 'sujet', 'statut')
    list_filter = ('type_destinataire', 'statut', 'date')
    search_fields = (
        'patient__utilisateur__first_name',
        'patient__utilisateur__last_name',
        'kine__utilisateur__first_name',
        'kine__utilisateur__last_name',
        'vendeur__utilisateur__first_name',
        'vendeur__utilisateur__last_name',
        'sujet'
    )
    date_hierarchy = 'date'

    def get_patient(self, obj):
        return obj.patient.utilisateur.get_full_name()
    get_patient.short_description = 'Patient'

    def get_destinataire(self, obj):
        if obj.type_destinataire == 'KINE' and obj.kine:
            return obj.kine.utilisateur.get_full_name()
        elif obj.type_destinataire == 'VENDEUR' and obj.vendeur:
            return obj.vendeur.utilisateur.get_full_name()
        return '-'
    get_destinataire.short_description = 'Destinataire'
