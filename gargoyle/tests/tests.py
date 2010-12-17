from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache
from django.http import HttpRequest, Http404
from django.test import TestCase

from gargoyle.models import gargoyle, Switch
from gargoyle.decorators import switch_is_active
from gargoyle import autodiscover

autodiscover()

class GargoyleTest(TestCase):
    urls = 'gargoyle.urls'
    
    def setUp(self):
        self.user = User.objects.create(username='foo', email='foo@example.com')

    def test_builtin_discovery(self):
        # TODO: this test shoudl just ensure we've registered our builtins
        self.assertEquals(len(gargoyle._registry), 2)

    def test_user(self):
        gargoyle['test_user'] = {'auth.user': {'percent': [[0, 50]], 'is_staff': [True]}}

        user = User(pk=5)
        self.assertTrue(gargoyle.is_active('test_user', user))

        user = User(pk=8771)
        self.assertFalse(gargoyle.is_active('test_user', user))

    def test_decorator_for_user(self):
        @switch_is_active('switched_for_user')
        def test(request):
            return True

        request = HttpRequest()
        request.user = self.user

        self.assertRaises(Http404, test, request)

        gargoyle['switched_for_user'] = {}

        self.assertTrue(test(request))

        gargoyle['switched_for_user'] = {'auth.user': {'username': ['foo']}}

        self.assertTrue(test(request))

    def test_decorator_for_ip_address(self):
        @switch_is_active('switched_for_ipaddress')
        def test(request):
            return True

        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '192.168.1.1'

        self.assertRaises(Http404, test, request)

        gargoyle['switched_for_ipaddress'] = {'ip': {'ip_address': ['192.168.1.1']}}

        self.assertTrue(test(request))

        gargoyle['switched_for_ipaddress'] = {'ip': {'ip_address': ['127.0.0.1']}}

        self.assertRaises(Http404, test, request)

        gargoyle['switched_for_ipaddress'] = {}

        self.assertTrue(test(request))

        gargoyle['switched_for_ipaddress'] = {'ip': {'percent': [[50, 100]]}}

        self.assertTrue(test(request))

        gargoyle['switched_for_ipaddress'] = {'ip': {'percent': [[0, 50]]}}

        self.assertRaises(Http404, test, request)

    def test_global(self):
        gargoyle['test_for_all'] = {}

        self.assertTrue(gargoyle.is_active('test_for_all'))

        gargoyle['test_for_all'] = {'auth.user': {'username': ['dcramer']}}

        self.assertFalse(gargoyle.is_active('test_for_all'))

        gargoyle['test_for_all'] = {'auth.user': {'username': ['dcramer']}, 'global': True}

        self.assertTrue(gargoyle.is_active('test_for_all'))

    def test_disable(self):
        gargoyle['test_disable'] = {'global': False}

        self.assertFalse(gargoyle.is_active('test_disable'))

        self.assertFalse(gargoyle.is_active('test_disable', self.user))

    def test_expiration(self):
        gargoyle['test_expiration'] = {'global': False}

        self.assertFalse(gargoyle.is_active('test_expiration'))

        Switch.objects.filter(key='test_expiration').update(value={})

        # cache shouldn't have expired
        self.assertFalse(gargoyle.is_active('test_expiration'))

        # in memory cache shouldnt have expired
        cache.delete(gargoyle.cache_key)
        self.assertFalse(gargoyle.is_active('test_expiration'))

        # any request should expire the in memory cache
        self.client.get('/')

        self.assertTrue(gargoyle.is_active('test_expiration'))

    def test_anonymous_user(self):
        gargoyle['test_anonymous_user'] = {'global': False}

        user = AnonymousUser()

        self.assertFalse(gargoyle.is_active('test_anonymous_user', user))

        gargoyle['test_anonymous_user'] = {'auth.user': {'percent': [1, 10]}}

        self.assertFalse(gargoyle.is_active('test_anonymous_user', user))

        gargoyle['test_anonymous_user'] = {}

        self.assertTrue(gargoyle.is_active('test_anonymous_user', user))

        gargoyle['test_anonymous_user'] = {'auth.user': {'is_authenticated': False}}

        self.assertTrue(gargoyle.is_active('test_anonymous_user', user))

        gargoyle['test_anonymous_user'] = {'auth.user': {'percent': [1, 10], 'is_authenticated': False}}

        self.assertTrue(gargoyle.is_active('test_anonymous_user', user))

    def test_ip_address(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '192.168.1.1'

        self.assertFalse(gargoyle.is_active('test_ip_address', request))

        gargoyle['test_ip_address'] = {'ip': {'ip_address': ['192.168.1.1']}}

        self.assertTrue(gargoyle.is_active('test_ip_address', request))

        gargoyle['test_ip_address'] = {'ip': {'ip_address': ['127.0.1.1']}}

        self.assertFalse(gargoyle.is_active('test_ip_address', request))

        gargoyle['test_ip_address'] = {}

        self.assertTrue(gargoyle.is_active('test_ip_address', request))

        gargoyle['test_ip_address'] = {'ip': {'percent': [[50, 100]]}}

        self.assertTrue(gargoyle.is_active('test_ip_address', request))
        
        gargoyle['test_ip_address'] = {'ip': {'percent': [[0, 50]]}}
        
        self.assertFalse(gargoyle.is_active('test_ip_address', request))