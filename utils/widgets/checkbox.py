import math

from django.forms import widgets
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


# Heavily inspired on a Django snippet!
# See https://djangosnippets.org/snippets/2236/
class ColumnCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """
    Widget that renders multiple-select checkboxes in columns.
    Constructor takes number of columns and css class to apply
    to the <ul> elements that make up the columns.
    """

    def __init__(self, columns=10, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.columns = int(columns)
        self.css_class = css_class

    def render(self, name, value, attrs=None, renderer=None):
        column_sizes = _columnize(len(self.choices), self.columns)
        items = list(enumerate(self.choices))
        columns = []
        for column_size in column_sizes:
            columns.append(items[:column_size])
            items = items[column_size:]

        output = []
        css = 'style="display:flex; flex-direction: row; justify-content: space-between; align-items: flex-start"'
        output.append(f'<ul {css}>')
        for column in columns:
            output.append(f'<div>')
            for i, (option_value, option_label) in column:
                checkbox = widgets.CheckboxInput(
                    self.build_attrs(attrs),
                    check_test=lambda v: v in set([force_str(v) for v in value or []])
                )
                output.extend([
                    '<li>'
                    u'%s %s' % (
                        checkbox.render(name, force_str(option_value)),
                        conditional_escape(force_str(option_label))
                    ),
                    '</li>'
                ])
            output.append(u'</div>')
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


def _rowlanize(total, per_row):
    """
    Return a list containing numbers of elements per column if `items` items
    are to be divided into `columns` columns.

    >>> _rowlanize(10, 2)
    [2, 2, 2, 2, 2]
    >>> _rowlanize(10, 3)
    [3, 3, 3, 1]
    >>> _rowlanize(3, 4)
    [3]
    """

    # rowlanized = []
    # for range(0, total, per_row):
    #     rowlanized.append(per_row)

    return [per_row for i in range(0, total, per_row)]


def _columnize(items, columns):
    """
    Return a list containing numbers of elements per column if `items` items
    are to be divided into `columns` columns.

    >>> _columnize(10, 1)
    [10]
    >>> _columnize(10, 2)
    [5, 5]
    >>> _columnize(10, 3)
    [4, 3, 3]
    >>> _columnize(3, 4)
    [1, 1, 1, 0]
    """
    elts_per_column = []
    for col in range(columns):
        col_size = int(math.ceil(float(items) / columns))
        elts_per_column.append(col_size)
        items -= col_size
        columns -= 1
    return elts_per_column
