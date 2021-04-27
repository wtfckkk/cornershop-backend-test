from unittest import mock
from unittest.mock import patch

from celery.contrib.testing.worker import start_worker
from django.contrib.auth.models import User
from django.urls import reverse
from model_bakery import baker
from django.test import SimpleTestCase
from rest_framework.test import APIClient

from backend_test.celery import app
from meals.models import Menu, Employee
from meals.tasks import notify_menu


class MenuTest(SimpleTestCase):
    allow_database_queries = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app.loader.import_module('celery.contrib.testing.tasks')
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.menu = baker.make(Menu, country='CL')
        self.employee = baker.make(Employee, country='CL')

    def test_menu_model_creation(self):
        self.assertTrue(isinstance(self.menu, Menu))
        self.assertEqual(Menu.STATE_OPEN, self.menu.state)
        self.assertFalse(self.menu.published)

    def test_menu_list_without_login(self):
        response = self.client.get('/menu/list/', follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateNotUsed('menu_list.html')
        self.assertTemplateUsed('login.html')

    def test_menu_list_with_login(self):
        response = self.client.get('/menu/list/', follow=True)
        self.client.force_login(user=self.employee.user)
        self.assertEqual(200, response.status_code)
        self.assertTemplateNotUsed('login.html')
        self.assertTemplateUsed('menu_list.html')

    def test_menu_notify_to_slack_celery_task(self):
        conversation_open_response = {"ok": True, "channel": {"id": "1"}}
        chat_post_message_response = {"ok": True}
        with mock.patch('meals.tasks.WebClient.conversations_open', return_value=conversation_open_response) as mocked:
            with mock.patch('meals.tasks.WebClient.chat_postMessage', return_value=chat_post_message_response) as _:
                notify_menu.run(self.menu.id)
                self.assertTrue(mocked.assert_called_once())
                self.assertTrue(_.assert_called_once())
                self.assertTrue(self.menu.published)
