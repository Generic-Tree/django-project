from django.contrib.admin import *
from django.urls import reverse


class ModelAdmin(ModelAdmin):

    @property
    def app_label(self):
        return self.model._meta.app_label

    @property
    def model_name(self):
        return self.model._meta.model_name

    @property
    def admin_name(self):
        return self.admin_site.name

    def get_admin_view_name(self, view):
        return '%s:%s_%s_%s' % (
            self.admin_name,
            self.app_label,
            self.model_name,
            view
        )

    def get_admin_view_url(self, view, *args, **kwargs):
        return reverse(
            self.get_admin_view_name(view),
            urlconf=None,
            args=args,
            kwargs=kwargs,
            current_app=self.app_label
        )
