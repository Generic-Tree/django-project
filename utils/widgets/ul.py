from django.forms import widgets


class UnorderedList(widgets.Widget):
    template_name = "utils/widgets/ul.html"

    def __init__(self, attrs=None):
        super(UnorderedList, self).__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context
