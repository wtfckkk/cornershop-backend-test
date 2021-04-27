from django.contrib.auth.models import User

from meals.models import Order, Employee
from meals.serializers import OrderSerializer


class EmployeeOrderMealServiceException(object):
    pass


class EmployeeOrderMealService(object):

    def __init__(self, payload):
        self.payload = payload

    @classmethod
    def execute(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.process()

    def process(self):
        try:
            # Create an order data object from payload
            order_data = {
                "employee": Employee.objects.get(slack_user=self.payload['user']['id']).id,
                "meal": self.payload['actions'][0]['value'].split('*')[0],
                "menu": self.payload['actions'][0]['value'].split('*')[1]
            }

            # Serialize object and create Order if not exists
            order = Order.objects.filter(meal__id=order_data['meal'],
                                         menu__id=order_data['menu'],
                                         employee__id=order_data['employee'])
            if not order:
                serializer = OrderSerializer(data=order_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        except Exception as e:
            raise Exception(e)
