from django.test import TestCase
from kitchen.forms import (CategoryNameSearchForm,
                           DishNameSearchForm,
                           CookUsernameSearchForm
                           )


class SearchFormTests(TestCase):
    def test_category_name_search_form_valid_data(self):
        form_data = {
            'name': 'Test Category',
        }
        form = CategoryNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_dish_name_search_form_valid_data(self):
        form_data = {
            'name': 'Test Dish',
        }
        form = DishNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_username_search_form_valid_data(self):
        form_data = {
            'username': 'test_cook',
        }
        form = CookUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
