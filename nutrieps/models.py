from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# UserProfile (Relation 1 to 1 with User)
class UserProfile(models.Model):
    WEIGHT_GOAL_CHOICES = [
        ('L', 'Lose Weight (-300 kcal)'),
        ('M', 'Maintain Weight'),
        ('G', 'Gain Muscle (+300 kcal)'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link with the User table
    height = models.FloatField(help_text="Height in cm")  # Attribute
    weight = models.FloatField(help_text="Weight in kg")  # Attribute
    calories_goal = models.IntegerField(default=2000)  # Attribute
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
        help_text="Biological sex for BMR calculation"
    )  # Attribute
    goal_type = models.CharField(
        max_length=1,
        choices=WEIGHT_GOAL_CHOICES,
        default='M',
        help_text="User's weight goal"
    )  # Attribute

    class Meta:
        verbose_name = "User Profile"  # How it shows in the admin panel
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('nutrieps:profile')


# WeightLog (Relation Many to 1 with User)
class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link with the User table
    weight = models.FloatField(help_text="Weight in kg")  # Attribute
    date = models.DateField(auto_now_add=True)  # Automatically set to today

    class Meta:
        ordering = ['-date']  # Orders from newest to oldest

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg"

    def get_absolute_url(self):
        return reverse('nutrieps:profile')


# FoodItem (Independent entity -> Will act as a 'local cache' for saving the food, so don't need to req the api)
class FoodItem(models.Model):
    name = models.CharField(max_length=200)  # Attribute
    calories = models.FloatField(help_text="Kcal per 100g or serving")  # Attribute
    protein = models.FloatField(default=0)  # Attribute
    carbs = models.FloatField(default=0)  # Attribute
    fat = models.FloatField(default=0)  # Attribute

    class Meta:
        ordering = ['name']  # Orders alphabetically

    def __str__(self):
        return self.name


# ConsumptionLog (Relation Many to 1 with User and FoodItem)
class ConsumptionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link with the User table
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)  # Link with the FoodItem table
    date = models.DateField(auto_now_add=True)  # Automatically set to today
    quantity = models.FloatField(help_text="Quantity in grams")  # Attribute

    class Meta:
        ordering = ['-date']  # Orders from newest to oldest

    def __str__(self):
        return f"{self.user.username} consumed {self.food.name}"

    def get_absolute_url(self):
        # Redirects to the history page after logging food
        return reverse('nutrieps:history')
