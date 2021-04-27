from model_bakery import baker
from django.test import SimpleTestCase, client

from meals.models import Meal


class MealTest(SimpleTestCase):
    allow_database_queries = True

    def setUp(self):
        super().setUp()
        self.meal = baker.make(Meal, name='Rice with almonds')

    def test_meal_model_creation(self):
        self.assertTrue(isinstance(self.meal, Meal))
        self.assertEqual("Rice with almonds", self.meal.__str__())
