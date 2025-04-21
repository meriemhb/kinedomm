from django.db import models
from users.models import Utilisateur
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Appointment(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
        ('TERMINE', 'Terminé'),
    ]

    patient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='appointments_as_patient')
    kine = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='appointments_as_kine')
    date_heure = models.DateTimeField()
    duree = models.IntegerField(help_text="Durée en minutes")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.patient} avec {self.kine} le {self.date_heure}"

    def get_status_color(self):
        colors = {
            'EN_ATTENTE': 'warning',
            'CONFIRME': 'success',
            'ANNULE': 'danger',
            'TERMINE': 'info',
        }
        return colors.get(self.statut, 'secondary')

class Availability(models.Model):
    kine = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='availabilities')
    jour = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_rdv = models.IntegerField(
        default=30,
        validators=[MinValueValidator(15), MaxValueValidator(120)],
        help_text="Durée d'un rendez-vous en minutes"
    )
    est_disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Disponibilité"
        verbose_name_plural = "Disponibilités"
        ordering = ['jour', 'heure_debut']
        unique_together = ['kine', 'jour', 'heure_debut']
    
    def __str__(self):
        return f"Disponibilité de {self.kine} le {self.jour} de {self.heure_debut} à {self.heure_fin}"
    
    def get_creneaux_disponibles(self):
        """Retourne la liste des créneaux disponibles pour cette plage horaire"""
        creneaux = []
        current_time = self.heure_debut
        while current_time < self.heure_fin:
            creneaux.append(current_time)
            # Ajouter la durée du rendez-vous
            minutes = current_time.hour * 60 + current_time.minute + self.duree_rdv
            current_time = current_time.replace(
                hour=minutes // 60,
                minute=minutes % 60
            )
        return creneaux

class Conseil(models.Model):
    TYPE_CHOICES = [
        ('CONSEIL', 'Conseil'),
        ('VIDEO', 'Vidéo'),
        ('IMAGE', 'Image'),
    ]

    kine = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conseils')
    titre = models.CharField(max_length=200)
    type_contenu = models.CharField(max_length=10, choices=TYPE_CHOICES)
    contenu = models.TextField()
    media = models.FileField(upload_to='conseils/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    patients = models.ManyToManyField(Utilisateur, related_name='conseils_recus', blank=True)
    est_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Conseil"
        verbose_name_plural = "Conseils"
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.kine.get_full_name()}"

class TreatmentRequest(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé'),
    ]

    patient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='treatment_requests')
    kine = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='received_requests')
    description = models.TextField()
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement_souhaite = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    reponse = models.TextField(blank=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Demande de traitement"
        verbose_name_plural = "Demandes de traitement"
        ordering = ['-date_demande']

    def __str__(self):
        return f"Demande de {self.patient.get_full_name()} à {self.kine.get_full_name()}"
