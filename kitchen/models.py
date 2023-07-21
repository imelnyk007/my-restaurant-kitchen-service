from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    year_of_experience = models.IntegerField(null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="cook_photo/")

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(Cook, related_name="dishes", null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="dish_pictures/")

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ["category__name"]

    def __str__(self):
        return self.name
