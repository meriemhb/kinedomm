from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Patient, Kine, Vendeur, Admin

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'date_naissance', 'telephone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('role', 'date_naissance', 'telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('role', 'date_naissance', 'telephone')}),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_nom_complet', 'numero_securite_sociale')
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name')

    def get_nom_complet(self, obj):
        return obj.utilisateur.get_full_name()
    get_nom_complet.short_description = 'Nom complet'

@admin.register(Kine)
class KineAdmin(admin.ModelAdmin):
    list_display = ('get_nom_complet', 'numero_adeli', 'specialites')
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name')

    def get_nom_complet(self, obj):
        return obj.utilisateur.get_full_name()
    get_nom_complet.short_description = 'Nom complet'

@admin.register(Vendeur)
class VendeurAdmin(admin.ModelAdmin):
    list_display = ('get_nom_complet', 'entreprise')
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name')

    def get_nom_complet(self, obj):
        return obj.utilisateur.get_full_name()
    get_nom_complet.short_description = 'Nom complet'

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('get_nom_complet', 'niveau_acces')
    search_fields = ('utilisateur__username', 'utilisateur__first_name', 'utilisateur__last_name')

    def get_nom_complet(self, obj):
        return obj.utilisateur.get_full_name()
    get_nom_complet.short_description = 'Nom complet'
