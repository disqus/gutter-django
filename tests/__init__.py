from django.conf import settings
from example_project.settings import GUTTER_STORAGE
settings.configure(
    ROOT_URLCONF='example_project.urls',
    GUTTER_STORAGE=GUTTER_STORAGE
)