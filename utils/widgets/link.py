from django.forms import widgets
from django.urls import reverse
from django.utils.http import urlencode


class Link(widgets.Widget):
    template_name = "utils/widgets/link.html"

    def __init__(self, href, attrs=None):
        super(Link, self).__init__(attrs)
        self.href = href

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'href': self.href
        })
        return context


class ViewLink(Link):
    def __init__(self, viewname, attrs=None, *args, **kwargs):
        super(ViewLink, self).__init__(
            reverse(viewname, args=args, kwargs=kwargs),
            attrs
        )


class ParameterizedLink(Link):
    def __init__(self, href, query_params=None, attrs=None):
        super(ParameterizedLink, self).__init__(
            f'{href}?{urlencode(query_params)}',
            attrs
        )


class ParameterizedViewLink(ParameterizedLink):

    def __init__(self, viewname, query_params=None, attrs=None, *args, **kwargs):
        super(ParameterizedViewLink, self).__init__(
            reverse(viewname, args=args, kwargs=kwargs),
            query_params,
            attrs
        )
