# shopping-cart

Clone the repo
```bash
$ git clone https://github.com/vchrombie/django-behave-playground/
$ django-behave-playground
```

Install the project
```bash
$ poetry install
$ poetry shell
```

Django project setup
```bash
(.venv) $ makemigrations
(.venv) $ migrate
(.venv) $ createsuperuser # admin:admin
(.venv) $ python manage.py loaddata shopping_cart/fixtures/data.json
(.venv) $ server
```
