
# coding: utf-8

# python imports
from functools import wraps
import json

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# django imports
from django import template
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.template.loader import get_template
from django.template.context import Context
from django.utils.translation import ugettext_lazy as _

from wpadmin.utils import (
    get_admin_site_name, get_wpadmin_settings, are_breadcrumbs_enabled)

register = template.Library()


def wpadmin_render_custom_style(context):
    custom_style_path = get_wpadmin_settings(get_admin_site_name(context)) \
        .get('custom_style', None)
    if custom_style_path:
        return mark_safe('<link type="text/css" rel="stylesheet" href="%s" />'
                         % custom_style_path)
    else:
        return ''

register.simple_tag(takes_context=True)(wpadmin_render_custom_style)


class AreBreadcrumbsEnabledNode(template.Node):

    def render(self, context):
        context['wpadmin_are_breadcrumbs_enabled'] = are_breadcrumbs_enabled(
            get_admin_site_name(context))
        return ''


def wpadmin_are_breadcrumbs_enabled(parser, token):
    return AreBreadcrumbsEnabledNode()

register.tag('wpadmin_are_breadcrumbs_enabled', wpadmin_are_breadcrumbs_enabled)


def wpadmin_render_custom_title(context):
    # Translators: This is already translated in Django
    return get_wpadmin_settings(get_admin_site_name(context)) \
        .get('title', context.get('site_title', _('Django site admin')))

register.simple_tag(takes_context=True)(wpadmin_render_custom_title)

@register.filter
def classname(obj, arg=None):
    classname = obj.__class__.__name__.lower()
    if arg:
        if arg.lower() == classname:
            return True
        return False
    return classname

