from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import DishForm, CookCreationForm, CookUpdateForm, CategoryNameSearchForm, DishNameSearchForm, \
    CookUsernameSearchForm
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


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = CategoryNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Category.objects.all()
        form = CategoryNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("kitchen:category-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("kitchen:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("kitchen:category-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("category")
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = DishNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = CookUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.prefetch_related("dishes__category")
        form = CookUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cook.dishes.all()
    ):
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
