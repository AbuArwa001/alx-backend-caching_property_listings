from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        # Import signals to ensure they are registered
        import properties.signals
        print("Properties app is ready and signals are imported.")