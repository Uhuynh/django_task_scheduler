import pytest


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    from django.conf import settings
    settings.setenv('testing')
