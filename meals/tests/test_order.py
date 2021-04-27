from model_bakery import baker
from django.test import SimpleTestCase, client

from meals.models import Meal, Order, Employee, Menu


class OrderTest(SimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()
        self.order = baker.make(Order)

    def test_order_model_creation(self):
        self.assertTrue(isinstance(self.order.meal, Meal))
        self.assertTrue(isinstance(self.order.menu, Menu))
        self.assertTrue(isinstance(self.order.employee, Employee))
