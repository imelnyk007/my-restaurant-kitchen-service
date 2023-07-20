from django.shortcuts import render
from django.views import generic

from kitchen.models import Category, Dish, Cook


def index(request):

    num_category = Category.objects.count()
    num_dish = Dish.objects.count()
    num_cook = Cook.objects.count()

    context = {
        "num_category": num_category,
        "num_dish": num_dish,
        "num_cook": num_cook,
    }
    return render(request, "kitchen/index.html", context=context)


class CategoryListView(generic.ListView):
    model = Category


class DishListView(generic.ListView):
    model = Dish


class DishDetailView(generic.DetailView):
    model = Dish


class CookListView(generic.ListView):
    model = Cook


class CookDetailView(generic.DetailView):
    model = Cook
