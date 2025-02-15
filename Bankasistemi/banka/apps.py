from django.apps import AppConfig


class BankaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banka'

    def ready(self):
        from . import tasks
        tasks.start_periodic_data_update()
     