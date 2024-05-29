# Real-time chat application with Django

## Overview
This is a Django rest framework application for real-time chat between users.
It utilizes Django channels for handling WebSockets and Redis as a message broker.

## Project Structure
The project is structured as follows:

django-chat/
* chat
    * migrations
    * test
    * __init__.py
    * admin.py
    * apps.py
    * consumers.py
    * models.py
    * routing.py
    * serializers.py
    * urls.py
    * views.py
* django_chat
    * __init__.py
    * asgi.py
    * routing.py
    * settings.py
    * urls.py
    * wsgi.py
* users
    * migrations
    * test
    * __init__.py
    * admin.py
    * apps.py
    * forms.py
    * managers.py
    * models.py
    * serializers.py
    * urls.py
    * views.py
* .gitignore
* manage.py
* poetry.lock
* pyproject.toml
* readme.md

## Requirements

```
1. Python>=3.8
2. Django>=5.x
3. Postgres
4. Redis
```


## Basic Setup Instructions

1. **Install Poetry**

   If you don't have Poetry installed, you can install it using the following command:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   For more installation options, refer to the Poetry documentation.

2. **Clone the respository**
    Open your terminal or command prompt and navigate to the directory where you want to clone the repository. Then, run the following command to clone the repository:
    ```bash
    cd git clone https://github.com/Saurab-Shrestha/django-chat.git
    cd django-chat
    ```

3. **Install project dependencies**
    Since the repository already contains the poetry.lock and pyproject.toml files, you can install the project dependencies by running the following command:
    ```bash
    poetry install
    ```
    Poetry will install all the required dependencies listed in the `poetry.lock` file.
    
4. **Start the Django project**
    After installing the dependencies, you can start the Django project by running the following commands:
    ```
    poetry run python manage.py migrate
    poetry run python manage.py runserver
    ```
    Then, you can view every apis through `http://127.0.0.1:8000/schema/swagger-ui/`

