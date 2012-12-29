from django.conf import settings
settings.configure(
    ROOT_URLCONF='example_project.urls',
    INSTALLED_APPS=('gutter.django', 'nexus')
)