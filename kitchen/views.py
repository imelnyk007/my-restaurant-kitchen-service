from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import (
    DishForm,
    CookCreationForm,
    CookUpdateForm,
    CategoryNameSearchForm,
    DishNameSearchForm,
    CookUsernameSearchForm, DishUpdateForm,
)
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
    paginate_by = 8

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


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category


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
    template_name = "kitchen/dish_create_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


@login_required
def update_dish(request, pk):
    dish = get_object_or_404(Dish, id=pk)

    if request.method == 'POST':
        form = DishUpdateForm(request.POST, request.FILES, instance=dish)

        if form.is_valid():
            form.save()
            return redirect("kitchen:dish-detail", pk=dish.id)
    else:
        form = DishUpdateForm(instance=dish)

    return render(request, 'kitchen/dish_update_form.html', {'form': form})


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
    template_name = 'kitchen/cook_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cook = self.get_object()
        dishes = cook.dishes.all()
        categories = list(set(dish.category for dish in dishes))
        context['categories'] = categories
        return context


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:index")


def register_request(request):
    if request.method == 'GET':
        form = CookCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        form = CookCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('kitchen:index')
        else:
            return render(request, 'registration/register.html', {'form': form})


@login_required
def update_cook(request, pk):
    cook = Cook.objects.get(id=pk)

    if request.method == 'POST':
        form = CookUpdateForm(request.POST, request.FILES, instance=cook)

        if form.is_valid():
            form.save()
            return redirect("kitchen:cook-detail", pk=cook.id)
    else:
        form = CookUpdateForm(instance=request.user)

    return render(request, 'kitchen/cook_form.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('kitchen:index')


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
