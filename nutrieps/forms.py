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

    WEIGHT_GOAL_CHOICES = [
        ('L', 'Lose Weight (-300 kcal)'),
        ('M', 'Maintain Weight'),
        ('G', 'Gain Muscle (+300 kcal)'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    age = forms.IntegerField(label="Age", min_value=10, max_value=120)
    weight = forms.FloatField(label="Weight (kg)", min_value=30.0, max_value=300.0)
    height = forms.FloatField(label="Height (cm)", min_value=100.0, max_value=250.0)
    activity_level = forms.ChoiceField(choices=ACTIVITY_CHOICES, label="Activity level")
    goal_type = forms.ChoiceField(choices=WEIGHT_GOAL_CHOICES, label='Weight goal type')


class ConsumptionForm(forms.Form):
    food_name = forms.CharField(max_length=200)
    calories = forms.FloatField()
    protein = forms.FloatField(required=False, initial=0)
    carbs = forms.FloatField(required=False, initial=0)
    fat = forms.FloatField(required=False, initial=0)
    quantity = forms.FloatField(min_value=1, label="Quantity (g)")