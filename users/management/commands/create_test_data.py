from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Kine, Patient

class Command(BaseCommand):
    help = 'Crée des données de test pour l\'application'

    def handle(self, *args, **kwargs):
        # Supprimer les données existantes
        get_user_model().objects.all().delete()
        Kine.objects.all().delete()
        Patient.objects.all().delete()

        # Créer des kinésithérapeutes
        kines = [
            {
                'username': 'john.kine',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john@example.com',
                'role': 'KINE',
                'specialites': 'Kinésithérapie sportive, Rééducation post-opératoire'
            },
            {
                'username': 'marie.kine',
                'first_name': 'Marie',
                'last_name': 'Dubois',
                'email': 'marie@example.com',
                'role': 'KINE',
                'specialites': 'Kinésithérapie respiratoire, Rééducation neurologique'
            },
            {
                'username': 'pierre.kine',
                'first_name': 'Pierre',
                'last_name': 'Martin',
                'email': 'pierre@example.com',
                'role': 'KINE',
                'specialites': 'Kinésithérapie pédiatrique, Rééducation orthopédique'
            }
        ]

        for kine_data in kines:
            # Créer l'utilisateur
            user = get_user_model().objects.create_user(
                username=kine_data['username'],
                email=kine_data['email'],
                password='test1234',
                first_name=kine_data['first_name'],
                last_name=kine_data['last_name'],
                role=kine_data['role']
            )
            
            # Créer le profil kiné
            Kine.objects.create(
                utilisateur=user,
                numero_adeli='123456789',
                specialites=kine_data['specialites']
            )
            
            self.stdout.write(self.style.SUCCESS(f'Kinésithérapeute créé : {user.get_full_name()}'))

        # Créer un patient de test
        user = get_user_model().objects.create_user(
            username='test.patient',
            email='patient@example.com',
            password='test1234',
            first_name='Test',
            last_name='Patient',
            role='PATIENT'
        )
        
        # Créer le profil patient
        patient = Patient.objects.create(
            utilisateur=user,
            numero_securite_sociale='123456789012345'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Patient de test créé : {user.get_full_name()}'))
        
        # Créer un superutilisateur
        admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin1234',
            first_name='Admin',
            last_name='Admin',
            role='ADMIN'
        )
        
        self.stdout.write(self.style.SUCCESS('Superutilisateur créé')) 