# django-dynaconf
A simple Django app with Dynaconf integrated. The setup is based on Docker Compose.

---
## Table of contents

1. [What is Dynaconf?](#1-what-is-dynaconf)
2. [Dynaconf - Django Extension](#2-dynaconf---django-extension)
3. [Setup](#3-setup)  
  3.1. [Initialize Dynaconf](#31-initialize-dynaconf)  
  3.2. [Bring up the project](#32-bring-up-the-project)
4. [Clean up](#4-clean-up)
---

# 1. What is Dynaconf?
- [Dynaconf](https://www.dynaconf.com/) is a layered configuration system for Python applications - with strong 
support for [12-factor applications](https://12factor.net/config) and extensions for Flask and Django.
- Some advantages of using Dynaconf:
  - Strict separation of settings from code
  - Store parameters in multiple file formats (.toml, .json, .yaml, .ini and .py)
  - Layered **[environment]** system.
  - Environment variables can be used to override parameters.
  - Support for `.env` files to automate the export of environment variables.
  - Drop in extension for Django `conf.settings` object.
  - Powerful `$ dynaconf CLI` to help you manage your settings via console.

# 2. Dynaconf - Django Extension
- [Dynaconf extension for Django](https://www.dynaconf.com/django/) works by patching the `settings.py` file 
with dynaconf loading hooks
- The change is done on a single file and then in your whole project every time you call `django.conf.settings`
you will have access to dynaconf attributes and methods.
- Instead of defining all of our project settings in Django default `settings.py`:
  ````python
  # settings.py
  ...
  SEVRER='foo.com'
  FOO='bar'
  ...
  ````
  With Dynaconf, we can easily define the settings in `settings.{yaml, toml, ini, json, py}`, which can change
based on the environments, for example `[default]`, `[development]`, and `[production]`
  ````yaml
  # settings.yaml
  
  default:
    server: foo.com
    foo: bar
  
  development:
    server: devserver.com
    foo: bar dev
    
  production:
    server: prodserver.com
    foo: bar prod
  ````
# 3. Setup

## 3.1. Initialize Dynaconf
- Add `django` and `dynaconf` packages to `requirements.txt`, which will be installed via Docker.
  ````text
  # requirements.txt
  
  django==4.0.6
  dynaconf==3.1.9
  ````
- Append at the bottom of your Django project's `settings.py` the following code to initialize Dynaconf:
  ````python
  # settings.py
  ...
  
  # HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
  # Read more at https://www.dynaconf.com/django/
  import dynaconf  # noqa
  settings = dynaconf.DjangoDynaconf(__name__)  # noqa
  # HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
  ````
- A more advanced Dynaconf initialization can be found in `project/settings.py`. For more
configuration options, check out [Dynaconf configuration docs](https://www.dynaconf.com/configuration/#load_dotenv).
  ````python
  # settings.py
  ...
  
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
          Validator('ENVIRONMENT', is_in=('dev', 'test')),
      ]  # A list of validators to be triggered right after the Dynaconf initialization.
  )  # noqa
  
  #
  # HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
  #
  ````
- We can now define all of Django settings in `project/settings.yaml` across different environment
  ````yaml
  default:
    ENVIRONMENT:
  
    SECRET_KEY:
  
    ALLOWED_HOSTS: []
  
    INSTALLED_APPS:
      - django.contrib.admin
      - django.contrib.auth
      - django.contrib.contenttypes
      - django.contrib.sessions
      - django.contrib.messages
      - django.contrib.staticfiles
      - app.apps.AppConfig
    
    ...
  
  dev:
    SECRET_KEY: DEV-ENVIRONMENT-SECRET-KEY
  
  test:
    SECRET_KEY: TEST-ENVIRONMENT-SECRET-KEY
  ````
- It is possible to use environment variables to override parameters defined in `settings` file.
In our case, we use `.env` file to pass environment variables to our docker container.
  ````text
  # .env file
  
  DJANGO_DATABASES__default__USER=postgres-user
  DJANGO_DATABASES__default__PASSWORD=postgres-password
  DJANGO_DATABASES__default__NAME=postgres
  DJANGO_DATABASES__default__PORT=5432
  DJANGO_DATABASES__default__HOST=postgres-db
  ````
  Above variables will take precedence over those that are defined in `settings.yaml`:
  ````yaml
  default:
    DATABASES:
      default:
        ENGINE: django.db.backends.postgresql
        HOST: postgres
        NAME: postgres
        USER: postgres
        PASSWORD: postgres
        PORT: 5432
  ````
**Notes**:
- To access or change Dynaconf via environment variables, we can use the format 
`${ENVVAR_PREFIX}_${VARIABLE}__${NESTED_ITEM}__${NESTED_ITEM}`. Each `__` (dunder, a.k.a double underline) 
denotes access to nested elements in a dictionary.
- `DJANGO_` is used as the global prefix to export environment variables in this project.
- Django settings is case-sensitive, so `DYNACONF_DATABASES__default__ENGINE` is not the same as 
`DYNACONF_DATABASES__DEFAULT__ENGINE`
- `.yaml` is the recommended format for Django applications because it allows complex 
data structures
- To use `$ dynaconf` CLI the `DJANGO_SETTINGS_MODULE` environment variable must be defined.

## 3.2. Bring up the project
- Make sure to install `Docker` and `Docker Compose` on the machine
    ```bash
    $ docker --version
    Docker version 20.10.8, build 3967b7d
    $ docker-compose --version
    docker-compose version 1.29.2, build 5becea4c
    ```
- Clone the repository: https://github.com/Uhuynh/django-dynaconf
- Run `$ docker-compose up -d`
  - This will install required packages and bring up 2 services as defined in `docker-compose.yml`:
    - `app` is our Django application. Note that our Dynaconf environment switcher 
    `DJANGO_ENVIRONMENT` has to be defined as environment variable of the container
    - `postgres-db` is a PostgreSQL database for our Django application. Note how the environment variables 
    are defined in `environment` section.
- To verify the setup, go to `http://localhost:33000`. We should see below screen:

  ![home-page][homepage]
  - `SECRET_KEY` value is loaded from our `project/settings.yaml` under `[development]` environment
  - Database user is loaded from ``DJANGO_DATABASES__default__USER`` as defined in `.env` file, and not from
  `[default]` environment section of ``project/settings.yaml``.

# 4. Clean up
To clean up your environment (containers, volumes) run:
```shell
$ docker-compose down --volumes --remove-orphans
$ docker system prune
```
**Notes**:
- this will purge your volumes and all data

[homepage]: markdown/home.png