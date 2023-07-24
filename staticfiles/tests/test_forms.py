from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from kitchen.models import Category, Cook
from kitchen.forms import (DishForm,
                           DishUpdateForm,
                           CookCreationForm,
                           CookUpdateForm
                           )


class DishFormTests(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(
            username='test_cook',
            password='HytgvffhjH6754!^',
            first_name='Test',
            last_name='Cook',
            year_of_experience=5,
        )

        self.category = Category.objects.create(name='Test Category')

    def test_dish_form_valid_data(self):
        form_data = {
            'name': 'Test Dish',
            'description': 'This is a test dish.',
            'price': 12.9,
            'category': self.category,
            'cooks': [self.user],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_form_invalid_data(self):
        form_data = {
            'name': '',
            'description': 'This is a test dish.',
            'price': -5.00,
            'category': self.category.id,
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_dish_update_form_valid_data(self):
        form_data = {
            'name': 'Updated Dish',
            'description': 'This is an updated test dish.',
            'price': 15.9,
            'category': self.category,
            'cooks': [self.user],
        }
        form = DishUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_update_form_with_picture(self):
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form_data = {
            'name': 'Updated Dish',
            'description': 'This is an updated test dish.',
            'price': 15.9,
            'category': self.category,
            'cooks': [self.user],
            'picture': image,
        }
        form = DishUpdateForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_dish_update_form_invalid_data(self):
        form_data = {
            'name': '',
            'description': 'This is an updated test dish.',
            'price': -10.00,
            'category': self.category,
            'cooks': [self.user],
        }
        form = DishUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())


class CookFormTests(TestCase):
    def test_cook_creation_form_valid_data(self):
        form_data = {
            'username': 'new_cook',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'New',
            'last_name': 'Cook',
            'year_of_experience': 3,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_creation_form_invalid_data(self):
        form_data = {
            'username': 'new_cook',
            'password1': 'testpassword',
            'password2': 'different_password',
            'first_name': '',
            'last_name': 'Cook',
            'year_of_experience': -5,
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cook_update_form_valid_data(self):
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Cook',
            'year_of_experience': 6,
        }
        form = CookUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_update_form_with_photo(self):
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Cook',
            'year_of_experience': 6,
            'photo': image,
        }
        form = CookUpdateForm(data=form_data,)
        self.assertTrue(form.is_valid())

    def test_cook_update_form_invalid_data(self):
        form_data = {
            'first_name': '',
            'last_name': 'Cook',
            'year_of_experience': -10,
        }
        form = CookUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
