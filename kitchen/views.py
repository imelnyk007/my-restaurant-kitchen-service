from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import DishForm, CookCreationForm, CookUpdateForm
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


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("kitchen:category-list")


class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("kitchen:category-list")


class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = reverse_lazy("kitchen:category-list")


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("category")
    paginate_by = 3


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(generic.ListView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__category")
    paginate_by = 4


class CookDetailView(generic.DetailView):
    model = Cook


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
