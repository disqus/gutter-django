"""
gutter.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

from itertools import takewhile
import os

from gutter.client.default import gutter as manager
from gutter.django.forms import SwitchForm, ConditionFormSet, SwitchFormManager
import nexus
from collections import OrderedDict


class SwitchDict(OrderedDict):

    def set_switch(self, switch):
        self._switch = switch

    def get_switch(self, default=None):
        return getattr(self, '_switch', default)


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

        urlpatterns = patterns(
            '',
            url(r'^update/$', self.as_view(self.update), name='update'),
            url(r'^$', self.as_view(self.index), name='index'),
        )

        return urlpatterns

    def render_on_dashboard(self, request):
        return 'switches'

    @property
    def __index_context(self):
        switches = map(SwitchForm.from_object, manager.switches)
        new_switch = SwitchForm()
        new_switch.conditions = ConditionFormSet()

        switches = sorted(switches, key=lambda x: x.field('name'))

        seperator = manager.key_separator

        for i, switch in enumerate(switches):
            current = switch.field('name').split(manager.key_separator)

            if i == 0:
                depth = 0
            else:
                previous_switch = switches[i - 1]
                previous = previous_switch.field('name').split(manager.key_separator)
                depth = len(list(takewhile(lambda x: x[0] == x[1], zip(previous, current))))

            switch.depth = depth
            switch.prefix_depth = depth - 1

            switch.path = current
            switch.path_prefix = seperator.join(current[:depth])
            switch.path_leaf = seperator.join(current[depth:])

        def nest_switch(d, depth, switch):
            name = seperator.join(switch.path[:depth])
            d = d.setdefault(name, SwitchDict())

            if depth < len(switch.path):
                nest_switch(d, depth + 1, switch)
            else:
                d.set_switch(switch)

        d = SwitchDict()

        for switch in switches:
            nest_switch(d, 1, switch)

        return {
            "switches": switches,
            "switchdict": d,
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
