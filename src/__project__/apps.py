from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_module, module_has_submodule


class SourceApp(type):
    instances = {}
    prefix = None
    python_path = None

    def __new__(meta, python_path):
        """
        Factory that creates a SourceApp class from an provided module's AppConfig.
        """

        app_config = AppConfig.create(python_path)
        app_config_class = app_config.__class__

        sourceapp_name = app_config_class.__name__

        if sourceapp_name not in meta.instances:
            bases = (AppConfig,)
            attr = {
                var: getattr(app_config_class, var)
                for var in dir(app_config_class)
                if not var.startswith('__')
                   and getattr(app_config_class, var) != getattr(AppConfig, var, None)
            }
            attr.update({
                'python_path': python_path,
                'prefix': attr['prefix'] if 'prefix' in attr else python_path.split('.')[-1],
                '__init__': lambda self, *args:
                                super(self.__class__, self)
                                    .__init__(self.name, import_module(python_path))
            })

            meta.instances[sourceapp_name] = super(SourceApp, meta).__new__(meta, sourceapp_name, bases, attr)
        return meta.instances[sourceapp_name]

    @classmethod
    def collect(meta):
        """
        Declare a SourceApp class for each discovered Django App

        Return all them in a list
        """
        return [
            SourceApp(python_path)
            for python_path
            in meta.discover()
        ]

    @classmethod
    def discover(meta):
        """
        Look for Django App modules under APPS_ROOT path setting.

        Return the root python path of identified modules.
        """
        return [
            ".".join(
                path.parent
                    .relative_to(settings.APPS_ROOT)
                    .parts
            ) for path
            in settings.APPS_ROOT.glob('**/apps.py')
        ]

    def module(cls):
        return import_module(cls.python_path)

    def has(cls, submodule):
        return module_has_submodule(cls.module(), submodule)

    def urlpatterns(cls):
        if cls.has('urls'):
            from django.urls import path, include
            return path(cls.prefix + '/' if cls.prefix else '', include('%s.urls' % cls.python_path))

        raise ModuleNotFoundError()
