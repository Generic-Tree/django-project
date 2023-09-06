from django.utils.module_loading import autodiscover_modules

from .sites import LotteryAdminSite, site


def autodiscover():
    autodiscover_modules("admin", register_to=site)
