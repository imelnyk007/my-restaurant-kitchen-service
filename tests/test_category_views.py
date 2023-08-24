from django.test import TestCase
from django.urls import reverse
from kitchen.models import Category, Cook
from kitchen.forms import CategoryNameSearchForm


class CategoryViewTests(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

    def test_category_list_view(self):
        response = self.client.get(reverse('kitchen:category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/category_list.html')
        self.assertTrue('category_list' in response.context)

    def test_category_detail_view(self):
        url = reverse(
            'kitchen:category-detail',
            kwargs={'pk': self.category1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/category_detail.html')
        self.assertTrue('object' in response.context)

    def test_category_create_view(self):
        url = reverse('kitchen:category-create')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 3)

    def test_category_update_view(self):
        url = reverse(
            'kitchen:category-update',
            kwargs={'pk': self.category1.pk}
        )
        data = {'name': 'Updated Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Updated Category')

    def test_category_delete_view(self):
        url = reverse(
            'kitchen:category-delete',
            kwargs={'pk': self.category1.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)

    def test_category_list_view_with_search(self):
        url = reverse('kitchen:category-list')
        data = {'name': '1'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/category_list.html')
        self.assertTrue('category_list' in response.context)
        self.assertTrue('search_form' in response.context)
        self.assertIsInstance(
            response.context['search_form'],
            CategoryNameSearchForm
        )
        self.assertEqual(response.context['search_form'].initial['name'], '1')
