from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'date_naissance', 'telephone', 'password1', 'password2')
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=Utilisateur.Role.choices)
        self.fields['role'].initial = 'PATIENT'

class UserProfileForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'date_naissance', 'telephone')
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)  # Supprimer le champ password 