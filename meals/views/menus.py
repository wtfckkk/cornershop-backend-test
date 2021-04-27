from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from meals.forms import MenuForm
from meals.models import Menu
from meals.tasks import notify_menu


class MenuList(PermissionRequiredMixin, ListView):
    permission_required = 'meals.view_menu'
    template_name = "menu/menu_list.html"
    model = Menu
    ordering = ('-id', )


class MenuDetail(PermissionRequiredMixin, DetailView):
    permission_required = "meals.view_menu"
    template_name = "menu/menu_detail.html"
    model = Menu


class MenuCreation(PermissionRequiredMixin, CreateView):
    permission_required = "meals.add_menu"
    template_name = "menu/menu_form.html"
    form_class = MenuForm
    success_url = reverse_lazy('menu-list')


class MenuUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "meals.change_menu"
    template_name = "menu/menu_form.html"
    form_class = MenuForm
    queryset = Menu.objects.all()
    success_url = reverse_lazy('menu-list')


class MenuDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "meals.delete_menu"
    template_name = "menu/menu_confirm_delete.html"
    model = Menu
    success_url = reverse_lazy('menu-list')


class MenuNotifyToSlack(PermissionRequiredMixin, View):
    permission_required = "meals.add_menu"

    @staticmethod
    def get(request, *args, **kwargs):
        menu = get_object_or_404(Menu, id=kwargs['pk'])
        context = {'message': ""}
        if menu.can_publish():
            context['message'] = "Menu message send to Slack successfully !"
            notify_menu.delay(menu.id)
            return render(request, "menu/menu_confirm_publish.html", context)
        else:
            context['message'] = "Can't send to Slack a closed or published Menu"
            return render(request, "menu/menu_confirm_publish.html", context)
