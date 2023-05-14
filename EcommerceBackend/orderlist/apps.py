from django.apps import AppConfig


class OrderlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orderlist'

    def ready(self):
        import orderlist.signals
