from django.conf.urls.defaults import *

import nexus

from redis import Redis

from modeldict.redis import RedisDict

import gutter.client.settings

import gutter.web


# Configure Gutter
gutter.client.settings.manager.storage_engine = RedisDict('gutter', Redis())
gutter.web.autodiscover()

# Configure Nexus
nexus.autodiscover()

urlpatterns = patterns('',
    url(r'', include(nexus.site.urls)),
)
