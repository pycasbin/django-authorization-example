# Django-Authorization Example

[Django-authorization, or dauthz](https://github.com/pycasbin/django-authorization) is an authorization library for Django framework.

![image](https://user-images.githubusercontent.com/75596353/188881538-a6a99cb1-c88b-4738-bf4f-452be4fb7c2d.png)



## How To Run the Example

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Configure of Example: by step

### 1.add the django-orm-adapter and dauthz to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    # STEP1: setup adapter(django-orm-adapter here)
    'casbin_adapter.apps.CasbinAdapterConfig',
    # STEP2: setup django-authorization
    'dauthz.apps.DauthzConfig',
    # STEP3: setup the app of your app
    'user_management.apps.UserManagementConfig',
    ...
]
```

### 2.add the middlewares you need to MIDDLEWARES

```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # STEP2: setup django-authorization
    # be aware: should after AuthenticationMiddleware
    "dauthz.middlewares.request_middleware.RequestMiddleware",
    ...
]
```

### 3.add more config of adapter and dauthz

```python
# STEP1: setup adapter(django-orm-adapter here)
CASBIN_MODEL = os.path.join(BASE_DIR, 'dauthz_model.conf')
# STEP2: setup django-authorization
DAUTHZ = {
    # DEFAULT Dauthz enforcer
    "DEFAULT": {
        # Casbin model setting.
        "MODEL": {
            # Available Settings: "file", "text"
            "CONFIG_TYPE": "file",
            "CONFIG_FILE_PATH": CASBIN_MODEL,
            "CONFIG_TEXT": "",
        },
        # Casbin adapter.
        "ADAPTER": {
            "NAME": "casbin_adapter.adapter.Adapter",
        },
        "LOG": {
            # Changes whether Dauthz will log messages to the Logger.
            "ENABLED": False,
        },
    },
}
```

### 4. Add RBAC model to database(in /user_management/apps.py)

```python
p_rules = [
        ["anonymous", "/", "(GET)|(POST)"],
        ["anonymous", "/login", "(GET)|(POST)"],
        ["anonymous", "/register", "(GET)|(POST)"],
        ["normal_user", "/logout", "(GET)|(POST)"],
        ["admin", "/all_users_profile", "(GET)|(POST)"],
    ]
g_rules = [
    ["normal_user", "anonymous"],
    ["admin", "normal_user"]
]
enforcer.add_policies(p_rules)
enforcer.add_grouping_policies(g_rules)
enforcer.save_policy()
```

#### Model of Example : 

![image](https://user-images.githubusercontent.com/75596353/189869400-d7372ed9-99d1-4302-937a-dbc07e0d6fb4.png)

### 5. Completed.

## License

This project is licensed under the [Apache 2.0 license](https://github.com/php-casbin/laravel-authz/blob/master/LICENSE).