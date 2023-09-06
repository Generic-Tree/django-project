from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Customizing AdminSite
# See https://docs.djangoproject.com/en/dev/ref/contrib/admin/#adminsite-objects

class LotteryAdminSite(admin.AdminSite):
    site_header = _('Lottery')
    site_title = _('Lottery admin site')
    index_title = _('Lottery admin')
    # app_index_template = '.html'

    # empty_value_display = '-'
    # enable_nav_sidebar = False

    # login_template = ''
    # login_form =
    # logout_template = ''
    # password_change_template = ''
    # password_change_done_template = ''


site = LotteryAdminSite(name='lottery')
