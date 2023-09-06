from django.contrib.admin import apps
from django.utils.translation import gettext_lazy as _


class LotteryAdminConfig(apps.AdminConfig):
    default_site = 'lottery.sites.LotteryAdminSite'
    name = 'lottery'
    verbose_name = _('Lottery')

    default_auto_field = 'django.db.models.BigAutoField'
