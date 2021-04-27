from django.conf.urls import url
from rest_framework import routers
from .api.v1.views import SlackOAuthView, SlackEventsView
from .decorators import login_required

from .views.login import LoginView, LogoutView
from .views.meals import MealList, MealCreation, MealUpdate, MealDelete
from .views.menus import MenuList, MenuDetail, MenuCreation, MenuUpdate, MenuDelete, MenuNotifyToSlack
from .views.orders import OrderList
from .views import index

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^$', login_required(index), name='index'),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^slack/login/$', SlackOAuthView.as_view(), name='slack-login'),
    url(r'^slack/events/$', SlackEventsView.as_view(), name='slack-events'),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
]

menu_urlpatterns = [
    url(r'^menu/$', login_required(MenuList.as_view())),
    url(r'^menu/list/$', login_required(MenuList.as_view()), name='menu-list'),
    url(r'^menu/(?P<pk>\d+)/$', login_required(MenuDetail.as_view()), name='menu-detail'),
    url(r'^menu/new', login_required(MenuCreation.as_view()), name='menu-new'),
    url(r'^menu/edit/(?P<pk>\d+)/$', login_required(MenuUpdate.as_view()), name='menu-edit'),
    url(r'^menu/delete/(?P<pk>\d+)/$', login_required(MenuDelete.as_view()), name='menu-delete'),
    url(r'^menu/notify_slack/(?P<pk>\d+)/$', login_required(MenuNotifyToSlack.as_view()), name='menu-notify-slack'),
]

meal_urlpatterns = [
    url(r'^meal/$', login_required(MealList.as_view())),
    url(r'^meal/list/$', login_required(MealList.as_view()), name='meal-list'),
    url(r'^meal/new', login_required(MealCreation.as_view()), name='meal-new'),
    url(r'^meal/edit/(?P<pk>\d+)/$', login_required(MealUpdate.as_view()), name='meal-edit'),
    url(r'^meal/delete/(?P<pk>\d+)/$', login_required(MealDelete.as_view()), name='meal-delete'),
]

order_urlpatterns = [
    url(r'^order/$', login_required(OrderList.as_view())),
    url(r'^order/list/$', login_required(OrderList.as_view()), name='order-list'),
]

urlpatterns += router.urls
urlpatterns += menu_urlpatterns
urlpatterns += meal_urlpatterns
urlpatterns += order_urlpatterns

