from datetime import datetime

from celery.schedules import crontab
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from backend_test.celery import app
from backend_test.settings import SLACK_BOT_TOKEN
from meals.models import Menu, Employee, Order
from meals.serializers import OrderSerializer
from meals.utils import MenuMessage


"""Celery Beat Schedule.
    
"""
app.conf.beat_schedule = {
    'close_menu': {
        'task': 'meals.tasks.close_menu_by_date',
        'schedule': crontab(minute=0, hour=15),  # UTC Timezone
        'args': (datetime.today().strftime("%Y-%m-%d"),),
    }
}


@app.task
def close_menu_by_date(date):
    from .models import Menu
    for menu in Menu.objects.filter(date=datetime.strptime(date, "%Y-%m-%d"), state=Menu.STATE_OPEN):
        menu.close()


@app.task(bind=True)
def notify_menu(self, menu_id):
    """Celery Task.

       Sends the menu through Slack to employees in a specific
       country, also change state of the menu to published.

    """
    try:
        menu = Menu.objects.get(id=menu_id)
        menu_message = MenuMessage(menu).get_message_payload()

        client = WebClient(token=SLACK_BOT_TOKEN)

        # Sends Menu message to every employee
        employees = Employee.objects.filter(country=menu.country)
        for employee in employees:
            menu_message['users'] = [employee.slack_user]

            response = client.conversations_open(**menu_message)
            assert response["ok"] is True

            menu_message['channel'] = response['channel']['id']
            response = client.chat_postMessage(**menu_message)
            assert response["ok"] is True

        menu.to_published()

    except SlackApiError as e:
        raise Exception(f"Got an error: {e.response['error']}")

    except Exception as e:
        raise Exception(f"Got Exception: {e}")


@app.task()
def create_order(payload):
    try:
        # Create an order data object from slack payload
        order_data = {
            "employee": Employee.objects.get(slack_user=payload['user']['id']).id,
            "meal": payload['actions'][0]['value'].split('*')[0],
            "menu": payload['actions'][0]['value'].split('*')[1]
        }

        menu = Menu.objects.get(id=order_data['menu'])

        if menu.close:
            message = "Ups ! Too late... The Menu is closed"
            # TODO: Send response to Slack (hint: use payload['response_url'])

        order = Order.objects.filter(meal__id=order_data['meal'],
                                     menu__id=order_data['menu'],
                                     employee__id=order_data['employee'])

        if not order:
            serializer = OrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            message = f"Order ready, *{order.meal}* for launch today !"
            # TODO: Send response to Slack (hint: use payload['response_url'])
        else:
            message = f"You already order a Meal, *{order.meal}* for launch today !"
            # TODO: Send response to Slack (hint: use payload['response_url'])

    except Exception as e:
        raise Exception(f"Got Exception: {e}")

