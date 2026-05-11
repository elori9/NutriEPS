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


class DeleteConsumptionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')
        self.food = FoodItem.objects.create(name='Poma', calories=52, protein=0.3, carbs=14, fat=0.2)
        self.log = ConsumptionLog.objects.create(user=self.user, food=self.food, quantity=100)

    def test_delete_own_consumption(self):
        """Verifica que l'usuari pot eliminar el seu propi registre"""
        self.client.login(username='user1', password='pass')
        response = self.client.post(f'/history/delete/{self.log.id}/')
        self.assertFalse(ConsumptionLog.objects.filter(id=self.log.id).exists())

    def test_cannot_delete_other_users_consumption(self):
        """Verifica que no pots eliminar el registre d'un altre usuari (403)"""
        self.client.login(username='user2', password='pass')
        response = self.client.post(f'/history/delete/{self.log.id}/')
        self.assertEqual(response.status_code, 403)
        # L'objecte no s'ha d'haver eliminat
        self.assertTrue(ConsumptionLog.objects.filter(id=self.log.id).exists())

    def test_delete_requires_login(self):
        """Verifica que cal estar autenticat per eliminar"""
        response = self.client.post(f'/history/delete/{self.log.id}/')
        self.assertEqual(response.status_code, 302)  # Redirigeix al login

    def test_delete_confirmation_page_renders(self):
        """Verifica que la pàgina de confirmació es renderitza correctament (GET)"""
        self.client.login(username='user1', password='pass')
        response = self.client.get(f'/history/delete/{self.log.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poma')
        self.assertContains(response, 'Delete Food Log')

    def test_delete_redirects_to_history(self):
        """Verifica que després d'eliminar redirigeix a history"""
        self.client.login(username='user1', password='pass')
        response = self.client.post(f'/history/delete/{self.log.id}/')
        self.assertRedirects(response, '/history/')

    def test_cannot_view_other_users_delete_page(self):
        """Verifica que no pots veure la pàgina de confirmació d'un altre usuari"""
        self.client.login(username='user2', password='pass')
        response = self.client.get(f'/history/delete/{self.log.id}/')
        self.assertEqual(response.status_code, 403)
