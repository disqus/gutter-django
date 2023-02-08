from django.urls import include, path
from django.contrib import admin

import nexus

import gutter.django


# Configure Gutter
gutter.django.autodiscover()

# Configure Nexus
nexus.autodiscover()

urlpatterns = [
    path('', include(nexus.site.urls)),
    path('admin/', admin.site.urls),
]
