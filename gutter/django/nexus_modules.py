"""
gutter.nexus_modules
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from __future__ import absolute_import

import base64
import os
import pickle

from django.http import HttpResponse
from django.shortcuts import redirect
import nexus

from gutter.client.default import gutter as manager
from gutter.django.forms import SwitchForm, ConditionFormSet, SwitchFormManager


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
        try:
            from django.conf.urls import patterns, url
        except ImportError:
            from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns(
            '',
            url(r'^update/$', self.as_view(self.update), name='update'),
            url(r'^export/$', self.as_view(self.export_switches), name='export'),
            url(r'^import/$', self.as_view(self.import_switches), name='import'),
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
            return redirect('/gutter/')

        elif form_manager.is_valid():
            form_manager.save(manager)
            return redirect('/gutter/')

        else:
            return self.__render(request, invalid_manager=form_manager)

    def export_switches(self, request):
        switch_names = request.GET.getlist('switch')

        if switch_names:
            switches = [manager[name] for name in switch_names]
        else:
            switches = manager.switches

        pickled_switches = pickle.dumps(switches)
        encoded_switches = base64.b64encode(pickled_switches)

        switch_block = [encoded_switches[i:i + 64] for i in range(0, len(encoded_switches), 64)]
        switch_block.insert(0, '-----BEGIN SWITCHES-----')
        switch_block.append('-----END SWITCHES-----')

        switch_block = '\n'.join(switch_block)

        response = HttpResponse(switch_block)
        response['Content-Type'] = 'text/plain'
        response['Content-Length'] = len(switch_block)

        return response

    def import_switches(self, request):
        encoded_switches = request.POST.get('switch_block', '')
        switch_block = encoded_switches.split('\r\n')

        if switch_block[0] != '-----BEGIN SWITCHES-----' or switch_block[-1] != '-----END SWITCHES-----':
            raise ValueError('bad input')

        switch_block = ''.join(switch_block[1:-1])

        pickled_switches = base64.b64decode(switch_block)
        switches = pickle.loads(pickled_switches)

        for switch in switches:
            try:
                manager.register(switch)
            except Exception as e:
                print e

        return redirect('/gutter')

nexus.site.register(GutterModule, 'gutter')
