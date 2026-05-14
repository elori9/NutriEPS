from django.contrib.auth.models import User
from django.test import TestCase, Client
from nutrieps.models import FoodItem, ConsumptionLog, UserProfile


class NutriEpsCalculationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username="user1", password="password")


        self.pizza = FoodItem.objects.create(name="Pizza", calories=250, protein=10, carbs=30, fat=10)

        ConsumptionLog.objects.create(user=self.user1, food=self.pizza, quantity=200)
        ConsumptionLog.objects.create(user=self.user1, food=self.pizza, quantity=50)

    def test_daily_calories_computation(self):
        """ Check that the calorie sum is calculated correctly."""
        self.client.login(username="user1", password="password")

        response = self.client.get('/')


        self.assertEqual(response.context['calories_consumed'], 625)

    def test_bmr_calculation_male(self):
        """Check the metabolic rate calculation for a man"""
        self.client.login(username="user1", password="password")

        self.client.post('/profile/', {
            'gender': 'M',
            'age': 25,
            'weight': 80,
            'height': 180,
            'activity_level': '1.2',
            'goal_type': 'M',
        })

        profile = UserProfile.objects.get(user=self.user1)
        self.assertEqual(profile.calories_goal, 2166)

    def test_bmr_calculation_female_lose_weight(self):
        """Check the mathematical calculation for a woman who wants to lose weight."""
        self.client.login(username="user1", password="password")

        self.client.post('/profile/', {
            'gender': 'F',
            'age': 30,
            'weight': 60,
            'height': 160,
            'activity_level': '1.55',
            'goal_type': 'L',
        })

        profile = UserProfile.objects.get(user=self.user1)
        self.assertEqual(profile.calories_goal, 1698)