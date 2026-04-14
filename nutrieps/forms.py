# nutrieps/forms.py
from django import forms

class UserProfileForm(forms.Form):
    # Activity level options (for Harris-Benedict / Mifflin-St Jeor formula)
    ACTIVITY_CHOICES = [
        ('1.2', 'Sedentary (little or no exercise)'),
        ('1.375', 'Lightly active (light exercise 1-3 days/week)'),
        ('1.55', 'Moderately active (moderate exercise 3-5 days/week)'),
        ('1.725', 'Very active (vigorous exercise 6-7 days/week)'),
        ('1.9', 'Extra active (very hard physical work or double training)')
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Sexe")
    age = forms.IntegerField(label="Age", min_value=10, max_value=120)
    weight = forms.FloatField(label="Weight (kg)", min_value=30.0, max_value=300.0)
    height = forms.FloatField(label="Height (cm)", min_value=100.0, max_value=250.0)
    activity_level = forms.ChoiceField(choices=ACTIVITY_CHOICES, label="Activity level")