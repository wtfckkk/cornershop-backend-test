from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from meals.forms import MealForm
from meals.models import Meal


class MealList(PermissionRequiredMixin, ListView):
    permission_required = "meals.view_meal"
    template_name = "meal/meal_list.html"
    model = Meal
    queryset = Meal.objects.all()
    ordering = ('-id', )


class MealCreation(PermissionRequiredMixin, CreateView):
    permission_required = 'meals.add_meal'
    template_name = "meal/meal_form.html"
    form_class = MealForm
    success_url = reverse_lazy('meal-list')


class MealUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'meals.change_meal'
    template_name = "meal/meal_form.html"
    form_class = MealForm
    queryset = Meal.objects.all()
    success_url = reverse_lazy('meal-list')


class MealDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'meals.delete_meal'
    template_name = "meal/meal_confirm_delete.html"
    model = Meal
    success_url = reverse_lazy('meal-list')


