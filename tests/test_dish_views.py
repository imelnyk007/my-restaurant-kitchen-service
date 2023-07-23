from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from kitchen.models import Dish, Category, Cook
from kitchen.forms import DishNameSearchForm


class DishViewTests(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(username='test_user', password='HytgvffhjH6754!^')
        self.client = Client()
        self.client.login(username='test_user', password='HytgvffhjH6754!^')

        self.category = Category.objects.create(name='Test Category')

        self.dish1 = Dish.objects.create(
            name='Dish 1',
            description='Description 1',
            price=9.9,
            category=self.category,
        )
        self.dish2 = Dish.objects.create(
            name='Dish 2',
            description='Description 2',
            price=12.4,
            category=self.category)

    def test_dish_list_view(self):
        response = self.client.get(reverse('kitchen:dish-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/dish_list.html')
        self.assertTrue('dish_list' in response.context)
        self.assertEqual(Dish.objects.count(), 2)

    def test_dish_detail_view(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.dish1.picture = image
        self.dish1.save()

        url = reverse('kitchen:dish-detail', kwargs={'pk': self.dish1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/dish_detail.html')
        self.assertTrue('object' in response.context)

    def test_dish_create_view(self):
        url = reverse('kitchen:dish-create')
        dish_data = {
            "name": "Test Dish",
            "description": "This is a test dish.",
            "price": 10.99,
            "category": self.category.id,
            "cooks": [self.user.id],
        }

        response = self.client.post(url, data=dish_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.count(), 3)

    def test_dish_update_view(self):
        url = reverse('kitchen:dish-update', kwargs={'pk': self.dish1.id})
        data = {
            'name': 'Updated Dish',
            'description': 'Updated Description',
            'price': 17.99,
            'category': self.category.id,
            "cooks": [self.user.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.dish1.refresh_from_db()
        self.assertEqual(self.dish1.name, 'Updated Dish')

    def test_dish_delete_view(self):
        url = reverse('kitchen:dish-delete', kwargs={'pk': self.dish1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.count(), 1)

    def test_dish_list_view_with_search(self):
        url = reverse('kitchen:dish-list')
        data = {'name': '1'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/dish_list.html')
        self.assertTrue('dish_list' in response.context)
        self.assertTrue('search_form' in response.context)
        self.assertIsInstance(response.context['search_form'], DishNameSearchForm)
        self.assertEqual(response.context['search_form'].initial['name'], '1')
