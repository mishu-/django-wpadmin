# coding: utf-8

"""
Dashboard template tags, the following dashboard tags are available:
 * ``{% wpadmin_render_dashboard %}``
 * ``{% wpadmin_render_dashboard_module %}``

To load the dashboard tags: ``{% load wpadmin_dashboard_tags %}``.
"""

# DJANGO IMPORTS
from django import template
from django.core.urlresolvers import reverse

# WPADMIN IMPORTS
from wpadmin.dashboard.utils import get_admin_site_name, get_index_dashboard

register = template.Library()
tag_func = register.inclusion_tag('wpadmin/dashboard/dummy.html', takes_context=True)


def wpadmin_render_dashboard(context, location='index', dashboard=None):
    """
    Template tag that renders the dashboard, it takes two optional arguments:

    ``location``
        The location of the dashboard, it can be 'index' (for the admin index
        dashboard) or 'app_index' (for the app index dashboard), the default
        value is 'index'.

    ``dashboard``
        An instance of ``Dashboard``, if not given, the dashboard is retrieved
        with the ``get_index_dashboard`` or ``get_app_index_dashboard``
        functions, depending on the ``location`` argument.
    """

    if dashboard is None:
        dashboard = get_index_dashboard(context)

    dashboard.init_with_context(context)

    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
wpadmin_render_dashboard = tag_func(wpadmin_render_dashboard)


def wpadmin_render_dashboard_module(context, module, index=None, subindex=None):
    """
    Template tag that renders a given dashboard module, it takes a
    ``DashboardModule`` instance as first parameter and an integer ``index`` as
    second parameter, that is the index of the module in the dashboard.
    """

    module.init_with_context(context)
    context.update({
        'template': module.template,
        'module': module,
        'index': index,
        'subindex': subindex,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
wpadmin_render_dashboard_module = tag_func(wpadmin_render_dashboard_module)
