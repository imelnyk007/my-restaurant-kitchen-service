from django.test import TestCase
from kitchen.models import Category, Cook, Dish


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')


class CookModelTest(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create(
            username='test_cook',
            year_of_experience=5
        )

    def test_cook_get_absolute_url(self):
        url = self.cook.get_absolute_url()
        self.assertEqual(url, f'/cooks/{self.cook.pk}/')


class DishModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test Category')
        cook = Cook.objects.create(username='test_cook', year_of_experience=5)
        self.dish = Dish.objects.create(
            name='Test Dish',
            price=10.99,
            category=category
        )
        self.dish.cooks.add(cook)

    def test_dish_str_method(self):
        self.assertEqual(str(self.dish), 'Test Dish')
