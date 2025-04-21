from django.db import models
from users.models import Patient, Kine, Vendeur
from django.utils.translation import gettext_lazy as _

class Reclamation(models.Model):
    class TypeDestinataire(models.TextChoices):
        KINE = 'KINE', _('Kinésithérapeute')
        VENDEUR = 'VENDEUR', _('Vendeur')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reclamations')
    type_destinataire = models.CharField(
        max_length=10,
        choices=TypeDestinataire.choices,
        default=TypeDestinataire.KINE
    )
    kine = models.ForeignKey(
        Kine, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reclamations_recues'
    )
    vendeur = models.ForeignKey(
        Vendeur, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reclamations_recues'
    )
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)
    sujet = models.CharField(max_length=200)
    description = models.TextField()
    statut = models.CharField(
        max_length=20,
        choices=[
            ('NOUVELLE', 'Nouvelle'),
            ('EN_COURS', 'En cours de traitement'),
            ('RESOLUE', 'Résolue'),
            ('FERMEE', 'Fermée'),
        ],
        default='NOUVELLE'
    )
    reponse = models.TextField(blank=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date', '-heure']
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Réclamations'

    def __str__(self):
        destinataire = self.kine.utilisateur.get_full_name() if self.kine else self.vendeur.utilisateur.get_full_name()
        return f"Réclamation de {self.patient.utilisateur.get_full_name()} contre {destinataire} - {self.sujet}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.type_destinataire == self.TypeDestinataire.KINE and not self.kine:
            raise ValidationError("Un kinésithérapeute doit être spécifié pour une réclamation de type KINE")
        if self.type_destinataire == self.TypeDestinataire.VENDEUR and not self.vendeur:
            raise ValidationError("Un vendeur doit être spécifié pour une réclamation de type VENDEUR")
