"""
gutter.templatetags.gutter_helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""
import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


def raw(parser, token):
    # Whatever is between {% raw %} and {% endraw %} will be preserved as
    # raw, unrendered template code.
    text = []
    parse_until = 'endraw'
    tag_mapping = {
        template.TOKEN_TEXT: ('', ''),
        template.TOKEN_VAR: ('{{', '}}'),
        template.TOKEN_BLOCK: ('{%', '%}'),
        template.TOKEN_COMMENT: ('{#', '#}'),
    }
    # By the time this template tag is called, the template system has already
    # lexed the template into tokens. Here, we loop over the tokens until
    # {% endraw %} and parse them to TextNodes. We have to add the start and
    # end bits (e.g. "{{" for variables) because those have already been
    # stripped off in a previous part of the template-parsing process.
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == template.TOKEN_BLOCK and token.contents == parse_until:
            return template.TextNode(u''.join(text))
        start, end = tag_mapping[token.token_type]
        text.append(u'%s%s%s' % (start, token.contents, end))
    parser.unclosed_block_tag(parse_until)
raw = register.tag(raw)


def render_field(field, value=None):
    return field.render(value)
render_field = register.filter(render_field)


def sort_by_key(field, currently):
    is_negative = currently.find('-') == 0
    current_field = currently.lstrip('-')

    if current_field == field and is_negative:
        return field
    elif current_field == field:
        return '-' + field
    else:
        return field

sort_by_key = register.filter(sort_by_key)


def sort_field(sort_string):
    return sort_string.lstrip('-')

sort_field = register.filter(sort_field)


@register.filter
@stringfilter
def rereplace(string, args):
    search = args.split(args[0])[1]
    replace = args.split(args[0])[2]

    return re.sub(search, replace, string)


@register.filter
@stringfilter
def replace(string, args):
    return string.replace(args[0], args[-1])


@register.filter
@stringfilter
def greyout(string):
    split = string.rsplit(":", 1)
    if len(split) > 1:
        s = '<span class="grey">{}:</span>{}'.format(*split)
    else:
        s = string
    return s
