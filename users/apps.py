from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):                #This is necessary for signals to work
        import users.signals
