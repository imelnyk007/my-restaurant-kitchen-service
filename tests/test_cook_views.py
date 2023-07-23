from django.test import TestCase, Client
from django.urls import reverse
from kitchen.models import Cook
from kitchen.forms import CookCreationForm, CookUpdateForm


class CookListViewTest(TestCase):
    def setUp(self):
        self.user = Cook.objects.create_user(
            username='test_user',
            password='HytgvffhjH6754!^'
        )
        self.client = Client()
        self.client.login(username='test_user', password='HytgvffhjH6754!^')

        self.cook1 = Cook.objects.create_user(
            username="cook1",
            password="password"
        )
        self.cook2 = Cook.objects.create_user(
            username="cook2",
            password="password"
        )
        self.cook3 = Cook.objects.create_user(
            username="testcook",
            password="password"
        )

    def test_cook_list_view(self):
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_list.html")
        self.assertEqual(len(response.context["cook_list"]), 4)

    def test_cook_list_view_with_search(self):
        response = self.client.get(
            reverse("kitchen:cook-list"), {"username": "testcook"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("cook_list", response.context)
        self.assertEqual(len(response.context["cook_list"]), 1)
        self.assertEqual(response.context["cook_list"][0], self.cook3)

    def test_cook_detail_view(self):
        response = self.client.get(
            reverse("kitchen:cook-detail", kwargs={"pk": self.cook1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/cook_detail.html")
        self.assertEqual(response.context["cook"], self.cook1)

    def test_cook_delete_view(self):
        response = self.client.get(
            reverse("kitchen:cook-delete", kwargs={"pk": self.cook1.pk})
        )
        self.assertTemplateUsed(response, "kitchen/cook_confirm_delete.html")
        response = self.client.post(
            reverse("kitchen:cook-delete", kwargs={"pk": self.cook1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cook.objects.filter(pk=self.cook1.pk).exists())

    def test_cook_creation_form(self):
        form_data = {
            "username": "newcook",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "New",
            "last_name": "Cook",
            "year_of_experience": 5,
        }

        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        cook = form.save()
        self.assertEqual(cook.username, "newcook")
        self.assertEqual(cook.first_name, "New")
        self.assertEqual(cook.last_name, "Cook")
        self.assertEqual(cook.year_of_experience, 5)
        self.assertTrue(Cook.objects.filter(username="newcook").exists())

    def test_cook_update_form(self):
        form_data = {
            "first_name": "Updated",
            "year_of_experience": 10,
        }

        form = CookUpdateForm(data=form_data, instance=self.cook1)
        self.assertTrue(form.is_valid())
        form.save()

        updated_cook = Cook.objects.get(pk=self.cook1.id)
        self.assertEqual(updated_cook.first_name, "Updated")
        self.assertEqual(updated_cook.year_of_experience, 10)
