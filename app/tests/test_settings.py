
def test_secret_key_setting():
    from django.conf import settings
    assert settings.SECRET_KEY == 'TEST-ENVIRONMENT-SECRET-KEY'
