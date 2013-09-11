"""
gutter.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

import os

from gutter.client.default import gutter as manager
from gutter.django.forms import SwitchForm, ConditionFormSet, SwitchFormManager
import nexus


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
            url(r'^update/$', self.as_view(self.update), name='update'),
            url(r'^$', self.as_view(self.index), name='index'),
        )

        return urlpatterns

    def render_on_dashboard(self, request):
        return 'switches'

    @property
    def __index_context(self):
        switches = map(SwitchForm.from_object, manager.switches)
        switches = sorted(switches, key=lambda x: x.field('name'))

        new_switch = SwitchForm()
        new_switch.conditions = ConditionFormSet()

        return {
            "switches": switches,
            "new_switch": new_switch
        }

    def __render(self, request, invalid_manager=None, **notices):
        context = self.__index_context
        template = "gutter/index.html"

        context.update(notices=notices)

        if invalid_manager:
            invalid_manager.add_to_switch_list(context['switches'])
            context['notices']['error'] = 'Unable to save switch.'

        return self.render_to_response(template, context, request)

    def index(self, request):
        return self.__render(request)

    def update(self, request):
        form_manager = SwitchFormManager.from_post(request.POST)

        if form_manager.switch.data.get('delete'):
            print request.POST
            manager.unregister(form_manager.switch.data['name'])
            return self.__render(request, success='Switch deleted successfully.')
        elif form_manager.is_valid():
            form_manager.save(manager)
            return self.__render(request, success='Switch saved successfully.')
        else:
            return self.__render(request, invalid_manager=form_manager)


nexus.site.register(GutterModule, 'gutter')
