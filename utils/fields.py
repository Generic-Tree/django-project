from django.core import validators
from django.db.models import query, aggregates, expressions
from django.db.models.fields import *
from django.utils import timezone, functional
from django.utils.translation import gettext_lazy as _


class FutureDateTimeField(DateTimeField):
    validators = [
        validators.MinValueValidator(timezone.now())
    ]


# Heavily inspired on open-source published package `django-models-extensions`
# See https://github.com/lampofearth/django-models-extensions/blob/master/django_models_extensions/models/fields/__init__.py#L11

class VirtualFunctionField(Field):
    empty_strings_allowed = False
    is_function = True
    description = _("Virtual function field. Returns function result ")

    def __init__(self, verbose_name=None, name=None, function=None,
                 output_field=None, **kwargs):
        self.output_field = output_field
        self.function = expressions.ExpressionWrapper(function, output_field)
        self.function.target = self
        super().__init__(verbose_name, name, **kwargs)

    def get_internal_type(self):
        return "VirtualFunctionField"

    def db_type(self, connection):
        return None

    def validate(self, value, model_instance):
        pass

    def formfield(self, **kwargs):
        return None

    def contribute_to_class(self, cls, name, private_only=True):
        super().contribute_to_class(cls, name, private_only)

    @functional.cached_property
    def cached_col(self):
        _qs = query.QuerySet(model=self.model)
        _qs._fields = set(['id'], )
        _qs = _qs.annotate(
            **{self.attname: self.function}).values_list(self.attname)
        return _qs.query.annotations[self.attname]

    def get_col(self, alias, output_field=None):
        return self.cached_col


class RelationCountField(VirtualFunctionField):
    description = _('Return named relation count')

    def __init__(self, relation_field, verbose_name=None, name=None):
        super().__init__(
            verbose_name,
            name,
            aggregates.Count(relation_field),
            IntegerField()
        )
