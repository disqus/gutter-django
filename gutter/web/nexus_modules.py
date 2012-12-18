"""
gutter.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

import nexus
import os

from gutter.client.default import gutter as manager
from gutter.web.forms import SwitchForm, ConditionFormSet, SwitchFormManager
from django.template import RequestContext
# from django.http import HttpResponse, HttpResponseNotFound


def operator_info(operator):
    return dict(
        path=operator,
        label=operator.label,
        preposition=operator.preposition,
        arguments=operator.arguments,
        group=operator.group
    )


def argument_info(argument_container):
    return dict(
        string=argument_container.__name__,
        arguments=argument_container.arguments
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
            url(r'^$', self.as_view(self.index), name='index'),
        )

        return urlpatterns

    def render_on_dashboard(self, request):
        return 'switches'

    @property
    def __index_context(self):
        return {
            "manager": manager,
            "sorted_by": 'date_created',
            "switches": dict((s.name, SwitchForm.from_object(s)) for s in manager.switches)
        }

    def __render(self, request, invalid_manager=None, **notices):
        context = self.__index_context
        template = "gutter/index.html"

        if invalid_manager:
            invalid_manager.replace_in_context(context['switches'])

        context.update(notices=notices)

        return self.render_to_response(template, context, request)

    def index(self, request):
        return self.__render(request)

    def update(self, request):
        form_manager = SwitchFormManager.from_post(request.POST)

        if form_manager.is_valid():
            form_manager.save(manager)
            return self.__render(request, succcess='Switch saved successfully.')
        else:
            return self.__render(request, invalid_manager=form_manager)

    add = update  # gutter_manger.register(switch) will replace or add based on the name

    def delete(self, request):
        # Have a delete checkbox that is there, but hidden with JS.  Clicking
        # the delete button selects the checkbox with JS and submits the form.
        pass

nexus.site.register(GutterModule, 'gutter')
