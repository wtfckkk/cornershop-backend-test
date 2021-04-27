import json

from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from backend_test.settings import SLACK_CLIENT_ID, SLACK_CLIENT_SECRET_ID, SLACK_OAUTH_REDIRECT_URI, LOGIN_URL
from meals.models import Menu, Meal, Order, Employee
from meals.serializers import MenuSerializer, MealSerializer, OrderSerializer, SlackEmployeeSerializer
from meals.tasks import notify_menu, create_order
from meals.utils import MenuMessage


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True)
    def publish(self, _request, pk):
        menu = get_object_or_404(Menu, id=pk)
        notify_menu.delay(menu.id)
        return Response('OK')


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class MealsViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]


class SlackOAuthView(APIView):

    authentication_classes = []

    def get(self, request):
        """Slack O-Auth.

               Authenticate an Slack user
           """

        code_param = request.GET.get('code', '')
        error = request.GET.get('error', '')
        if error:
            return redirect(LOGIN_URL)

        client = WebClient()

        try:
            response = client.oauth_v2_access(
                client_id=SLACK_CLIENT_ID,
                client_secret=SLACK_CLIENT_SECRET_ID,
                code=code_param,
                redirect_uri=SLACK_OAUTH_REDIRECT_URI
            )
            client = WebClient(token=response['authed_user']['access_token'])
            response = client.users_identity()
            assert response['ok'] is True
            response = client.users_info(user=response.data['user']['id'])
            assert response['ok'] is True

            employee = Employee.objects.filter(slack_user=response.data['user']['id']).first()
            if not employee:
                serializer = SlackEmployeeSerializer(data=response.data)
                serializer.is_valid()
                employee = serializer.save()

                group_employees = Group.objects.get(name='employees')
                group_employees.user_set.add(employee.user)

        except SlackApiError as e:
            return Response(e.response.data, status=400)

        # Login the user
        login(request, employee.user)

        # Redirect
        next_url = request.GET.get('next', '')
        redirect_url = next_url if next_url else "index"
        return redirect(redirect_url)


class SlackEventsView(APIView):
    authentication_classes = []
    event_menu_message = MenuMessage(menu=None).text

    def post(self, request):
        """
        Listen events in Slack
        """
        payload = json.loads(request.data.dict()['payload'])

        # Validate if is a response of a Menu Message
        if payload['message']['text'] == self.event_menu_message:
            create_order.delay(payload)

        return Response("ok")
