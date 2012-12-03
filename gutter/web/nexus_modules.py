"""
gutter.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import nexus
import os
from gutter.client.singleton import gutter as manager
# from django.http import HttpResponse, HttpResponseNotFound


from arguments import User, Request


def get_all_operators():
    from gutter.client.operators.comparable import *
    from gutter.client.operators.identity import *
    from gutter.client.operators.misc import *

    return (Equals, Between, LessThan, LessThanOrEqualTo, MoreThan,
            MoreThanOrEqualTo, Truthy, Percent, PercentRange)


def operator_info(operator):
    return dict(
        path=operator,
        label=operator.label,
        preposition=operator.preposition,
        arguments=','.join(operator.arguments),
        group=operator.group
    )


def argument_info(argument):
    return dict(
        string=argument.__name__,
        variables=[func.__name__ for func in argument.variables]
    )


class GutterModule(nexus.NexusModule):
    home_url = 'index'
    name = 'gutter'
    media_root = os.path.normpath(os.path.join(os.path.dirname(__file__), 'media'))

    def get_title(self):
        return 'Gutter'

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
            url(r'^add/$', self.as_view(self.add), name='add'),
            url(r'^update/$', self.as_view(self.update), name='update'),
            url(r'^delete/$', self.as_view(self.delete), name='delete'),
            url(r'^status/$', self.as_view(self.status), name='status'),
            url(r'^conditions/add/$', self.as_view(self.add_condition), name='add-condition'),
            url(r'^conditions/remove/$', self.as_view(self.remove_condition), name='remove-condition'),
            url(r'^$', self.as_view(self.index), name='index'),
        )

        return urlpatterns

    def render_on_dashboard(self, request):
        return 'switches'

    def index(self, request):
        return self.render_to_response("gutter/index.html", {
            "manager": manager,
            "sorted_by": 'date_created',
            "operators": map(operator_info, get_all_operators()),
            "arguments": map(argument_info, (User, Request))
        }, request)

    def add(self, request):
        pass

    def update(self, request):
        pass

    def status(self, request):
        pass

    def delete(self, request):
        pass

    def add_condition(self, request):
        pass

    def remove_condition(self, request):
        pass

nexus.site.register(GutterModule, 'gutter')