from django.conf.urls.defaults import *

import nexus

from redis import Redis

from durabledict.redis import RedisDict

import gutter.client.settings

import gutter.django


# Configure Gutter
gutter.client.settings.manager.storage_engine = RedisDict('gutter', Redis())
gutter.django.autodiscover()

# Configure Nexus
nexus.autodiscover()

urlpatterns = patterns('',
    url(r'', include(nexus.site.urls)),
)
