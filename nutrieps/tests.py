from django.test import TestCase, Client
from django.contrib.auth.models import User
from nutrieps.models import ConsumptionLog, FoodItem


class EditConsumptionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')
        self.food = FoodItem.objects.create(name='Poma', calories=52, protein=0.3, carbs=14, fat=0.2)
        self.log = ConsumptionLog.objects.create(user=self.user, food=self.food, quantity=100)

    def test_edit_own_consumption(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 200})
        self.log.refresh_from_db()
        self.assertEqual(self.log.quantity, 200)

    def test_cannot_edit_other_users_consumption(self):
        self.client.login(username='user2', password='pass')
        response = self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 999})
        self.assertEqual(response.status_code, 403)

    def test_edit_updates_quantity(self):
        """Verifica que la quantitat s'actualitza correctament"""
        self.client.login(username='user1', password='pass')
        self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 250})
        self.log.refresh_from_db()
        self.assertEqual(self.log.quantity, 250)

    def test_edit_requires_login(self):
        """Verifica que cal estar autenticat per editar"""
        response = self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 250})
        self.assertEqual(response.status_code, 302)  # Redirigeix al login

    def test_cannot_edit_other_user_log(self):
        """Verifica que no pots editar el registre d'un altre usuari"""
        self.client.login(username='user2', password='pass')
        response = self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 999})
        self.assertEqual(response.status_code, 403)

    def test_edit_redirects_to_history(self):
        """Verifica que després d'editar redirigeix a history"""
        self.client.login(username='user1', password='pass')
        response = self.client.post(f'/history/edit/{self.log.id}/', {'quantity': 150})
        self.assertRedirects(response, '/history/')
