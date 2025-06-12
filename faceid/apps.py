from django.apps import AppConfig

from faceid import face_utils


class FaceidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "faceid"

    def ready(self):
        face_utils.load_faces()
