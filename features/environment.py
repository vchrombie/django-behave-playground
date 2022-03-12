import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopping_cart.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from behave import fixture, use_fixture

User = get_user_model()


class BaseTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.create_superuser(username='admin', password='admin')
        super(BaseTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        User.objects.filter().delete()
        super(BaseTestCase, cls).tearDownClass()


@fixture
def django_test_case(context):
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    context.selenium = webdriver.Firefox(options=firefox_options)

    context.test_case = BaseTestCase

    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()

    context.selenium.quit()

    del context.test_case


def before_all(context):
    django.setup()

    context.test_runner = DiscoverRunner()

    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    yield
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    use_fixture(django_test_case, context)
