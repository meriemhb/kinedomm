import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kine_project.settings')
django.setup()

from users.models import Utilisateur
from appointments.models import TreatmentRequest
from django.utils import timezone

# Créer une demande de traitement de test
patient = Utilisateur.objects.get(username='test.patient')
kine = Utilisateur.objects.get(username='kine')
request = TreatmentRequest.objects.create(
    patient=patient,
    kine=kine,
    description='Test de demande de traitement',
    date_traitement_souhaite=timezone.now().date()
)
print(f"Demande de traitement créée avec l'ID : {request.id}") 