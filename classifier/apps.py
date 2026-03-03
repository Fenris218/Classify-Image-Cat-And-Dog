from django.apps import AppConfig


class ClassifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classifier'

    def ready(self):
        import classifier.signals
        from classifier.signals import populate_dog_breeds
        # Tạo các giống chó mặc định
        populate_dog_breeds()
