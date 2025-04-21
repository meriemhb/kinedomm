from django.contrib import admin
from .models import Materiel, Commande, LigneCommande

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nom', 'prix', 'stock', 'disponible', 'get_vendeur')
    list_filter = ('disponible', 'vendeur')
    search_fields = ('numero', 'nom')

    def get_vendeur(self, obj):
        return obj.vendeur.utilisateur.get_full_name()
    get_vendeur.short_description = 'Vendeur'

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient', 'date_commande', 'statut', 'total')
    list_filter = ('statut', 'date_commande')
    search_fields = ('patient__utilisateur__first_name', 'patient__utilisateur__last_name')
    inlines = [LigneCommandeInline]
    date_hierarchy = 'date_commande'

    def get_patient(self, obj):
        return obj.patient.utilisateur.get_full_name()
    get_patient.short_description = 'Patient'
