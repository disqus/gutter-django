"""
chimera.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import nexus
import os
from chimera.client.singleton import chimera as manager
# from django.http import HttpResponse, HttpResponseNotFound


def operator_info(operator):
    return dict(
        path=operator,
        label=operator.label,
        preposition=operator.preposition,
        arguments=','.join(operator.arguments),
        group=operator.group
    )


def input_info(inpt):
    return dict(
        string=inpt.__name__,
        arguments=[func.__name__ for func in inpt.arguments()]
    )


class ChimeraModule(nexus.NexusModule):
    home_url = 'index'
    name = 'chimera'
    media_root = os.path.normpath(os.path.join(os.path.dirname(__file__), 'media'))

    def get_title(self):
        return 'Chimera'

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
        return self.render_to_response("chimera/index.html", {
            "manager": manager,
            "sorted_by": 'date_created',
            "operators": map(operator_info, manager.operators),
            "inputs": map(input_info, manager.inputs)
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

nexus.site.register(ChimeraModule, 'chimera')