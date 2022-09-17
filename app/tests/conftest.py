import pytest


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    # https://github.com/dynaconf/dynaconf/issues/491#issuecomment-745391955
    from django.conf import settings
    settings.setenv('testing')  # force the environment to be whatever you want