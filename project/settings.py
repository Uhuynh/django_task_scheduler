"""
https://docs.djangoproject.com/en/1.11/topics/settings/
https://docs.djangoproject.com/en/1.11/ref/settings/
https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# HERE STARTS DYNACONF EXTENSION LOAD
#

import dynaconf  # noqa
from dynaconf import Validator # noqa

settings = dynaconf.DjangoDynaconf(
    __name__,
    settings_files=[
        'settings.yaml'
    ],  # the path for the files you wish dynaconf to load the settings from
    env_switcher='DJANGO_ENVIRONMENT',  # set the variable to switch environment
    load_dotenv=True,  # if True, dynaconf will try to load the variables from a .env file.
    validators=[
        Validator('ENVIRONMENT', must_exist=True),
        Validator('DEBUG', is_type_of=bool),
        Validator('ENVIRONMENT', is_in=('development', 'testing')),
    ]  # A list of validators to be triggered right after the Dynaconf initialization.
)  # noqa

#
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
#
