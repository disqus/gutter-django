from django.conf.urls import include, patterns, url

import nexus

from redis import Redis

from durabledict.redis import RedisDict

import gutter.client.settings

import gutter.django


# Configure Gutter
gutter.client.settings.manager.storage_engine = RedisDict(keyspace='gutter', connection=Redis())
gutter.django.autodiscover()

# Configure Nexus
nexus.autodiscover()

urlpatterns = patterns('',
    url(r'', include(nexus.site.urls)),
)
