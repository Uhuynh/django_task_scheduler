# Django Task Scheduler
An example of a Django - Celery tool that lets you schedule REST requests for a given point in time in the future.

---
To start the project:
- Check if `docker` and `docker-compose` are installed on the machine:
    ```bash
    $ docker --version
    Docker version 20.10.8, build 3967b7d
    $ docker-compose --version
    docker-compose version 1.29.2, build 5becea4c
    ```
- Clone this repository
- Run `$ docker-compose up -d --build` to bring up the project
- Run ``$ docker-compose ps`` to make sure all 5 services / containers are up.
- Run ``$ docker-compose run --rm app python manage.py migrate`` to migrate the database.
- Run ``$ docker-compose run --rm app python manage.py create_users`` to generate our users
  - a non-superuser: username=`john` and password=`johnpassword`
  - a superuser: username=`admin` and password=`test1234`
- To verify the setup, go to `http://localhost:33000`
  - We should see a login page. Please log in with the non-superuser credentials
- After a successful login, we should see a form where we can specify a new REST request by 
entering two required arguments:
  - `Number of company name(s) to create:*` a random number of company names (min=1 and max=100)
  - `Execution time:*` the execution time of the request (should be in the future, timezone: Europe/Berlin)
  - Click `Submit` to submit a POST request to the server
- To check for tasks status, go to `http://localhost:33002` where we can see a
[Flower](https://pypi.org/project/flower/) dashboard showing pending as well as processed requests.
- To verify whether the desired amount of company names are generated:
  - go to `http://localhost:33000/admin`
  - login with the superuser credentials
  - check for the instances under `APP/Company names` and their `create_datetime`
  - Note that `Faker` is used to generate random names, therefore the values might not be unique.