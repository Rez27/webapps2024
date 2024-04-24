from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'


#def ready(self):


    #Post Migrate to  run custom pyfile.function_name to make admin. (Make a custom py file in register app and import first)