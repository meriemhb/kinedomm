from django.db import models
from users.models import Vendeur, Patient

class Materiel(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE, related_name='materiels')
    stock = models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Matériel'
        verbose_name_plural = 'Matériels'

    def __str__(self):
        return f"{self.nom} ({self.numero})"

class Commande(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='commandes')
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('EN_ATTENTE', 'En attente'),
            ('CONFIRMEE', 'Confirmée'),
            ('EN_PREPARATION', 'En préparation'),
            ('EXPEDIEE', 'Expédiée'),
            ('LIVREE', 'Livrée'),
            ('ANNULEE', 'Annulée'),
        ],
        default='EN_ATTENTE'
    )
    adresse_livraison = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-date_commande']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f"Commande #{self.id} - {self.patient.utilisateur.get_full_name()}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.materiel.nom} x{self.quantite}"
