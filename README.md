# Social Network

## General info

This project is a simple web application with REST API for creating, reading, updating and deleting information about users and posts, with the possibility to like posts, view user activity and likes analytics.

## Built with

* [Python 3.8](https://www.python.org/)
* [Django 3.2](https://www.djangoproject.com/)
* [PostgreSQL 13.2](https://www.postgresql.org/)

## Setup

1. Clone the repository:

```sh
$ git clone https://github.com/aaaaasv/social-network.git
$ cd social-network
```

2. Create a virtual environment:

```sh
$ python -m venv venv
$ source venv/bin/activate
```
Note: If you're using Windows, to activate virtual environment run:
```
venv/Scripts/activate
```

3. Install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt.

4. Once `pip` has finished downloading the dependencies, apply migrations and run the server:
```sh
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.

### Configuration

The default database used is SQLite, but you can change it simply by adding these settings to your environment variables:
* `SQL_ENGINE` - tested with the usage of django.db.backends.postgresql, for any other database backend see [django documentation](https://docs.djangoproject.com/en/3.2/ref/databases/)
* `SQL_DATABASE` - the name of the database
* `SQL_USER` - database user with required permissions
* `SQL_PASSWORD` - password for the user
* `SQL_HOST` (*localhost* by default)
* `SQL_PORT` (*5432* by default)


## Usage

On the `http://127.0.0.1:8000` page you can find documentation about endpoints available to you depending on your permissions (not authenticated < authenticated < admin).

### Authentication

To create a new user make a POST request to `api/users/`, to create a superuser run:

```sh
(venv)$ python manage.py createsuperuser
```

#### Basic Auth

The application's main purpose is API, accessible from outside, but you still can use it with the web interface, to do this - login on the page `api/api-auth/login/`.

#### JWT

The application supports JSON Web Tokens:
* `api/token/` - to get a new token (with username and password in the body)
* `api/token/refresh/` - to refresh old token


## Tests

```
(venv)$ python manage.py test
```