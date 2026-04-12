# nutrieps/forms.py
from django import forms

class UserProfileForm(forms.Form):
    # Opcions pel nivell d'activitat (per a la fórmula de Harris-Benedict / Mifflin-St Jeor)
    ACTIVITY_CHOICES = [
        ('1.2', 'Sedentari (poc o cap exercici)'),
        ('1.375', 'Lleugerament actiu (exercici lleuger 1-3 dies/setmana)'),
        ('1.55', 'Moderadament actiu (exercici moderat 3-5 dies/setmana)'),
        ('1.725', 'Molt actiu (exercici fort 6-7 dies/setmana)'),
        ('1.9', 'Extra actiu (feina física molt dura o doble entrenament)')
    ]

    GENDER_CHOICES = [
        ('M', 'Home'),
        ('F', 'Dona')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Sexe")
    age = forms.IntegerField(label="Edat", min_value=10, max_value=120)
    weight = forms.FloatField(label="Pes (kg)", min_value=30.0, max_value=300.0)
    height = forms.FloatField(label="Alçada (cm)", min_value=100.0, max_value=250.0)
    activity_level = forms.ChoiceField(choices=ACTIVITY_CHOICES, label="Nivell d'activitat")