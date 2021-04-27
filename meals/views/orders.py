from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from meals.models import Order, Employee


class OrderList(PermissionRequiredMixin, ListView):
    permission_required = 'meals.view_order'
    template_name = "order/order_list.html"
    model = Order
    queryset = Order.objects.all()
    ordering = ('-id', )

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.queryset.filter(employee__id=Employee.objects.get(user__id=self.request.user.id).id)
        return self.queryset



