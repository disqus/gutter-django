from django.urls import include, path

import nexus

import gutter.django


# Configure Gutter
gutter.django.autodiscover()

# Configure Nexus
nexus.autodiscover()

urlpatterns = [
    path('', include(nexus.site.urls)),
]
