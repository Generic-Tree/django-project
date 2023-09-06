from django.utils.translation import (
    gettext_lazy as _,
    pgettext as __
)

from lottery import models, forms, sites
from utils import admin, widgets

site = sites.site


@admin.register(models.Bet, site=sites.site)
class BetAdmin(admin.ModelAdmin):
    form = forms.BetAdminForm

    list_display = ['tournament', 'id', 'bet_choices', 'registered_at']
    list_display_links = ['id', 'bet_choices']
    list_filter = ['tournament']

    def get_form(self, request, obj=None, change=False, **kwargs):
        return self.form.from_tournament(
            models.Tournament.objects.from_request(request)
        )


@admin.register(models.Tournament, site=sites.site)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['title', 'bet_count', 'start', 'list_actions']

    @admin.display(
        ordering='-bet_count',
        description=_('bet count'),
    )
    def bet_count(self, obj):
        # TODO: Improve link computation, probably with Templates
        link = widgets.ParameterizedViewLink(
            # BetAdmin(models.Bet, self.admin_site).get_admin_view_name('changelist'),
            'lottery:lottery_bet_changelist',
            {'tournament__id__exact': obj.id},
        )
        return link.render(_('bet count'), obj.bet_count)

    @admin.display(description=_('actions'))
    def list_actions(self, obj):
        # TODO: Improve link computation, probably with Templates
        link = widgets.ParameterizedViewLink(
            # BetAdmin(models.Bet, self.admin_site).get_admin_view_name('add'),
            'lottery:lottery_bet_add',
            {'tournament': obj.id},
        )
        return link.render('add_bet', __('action', 'bet'))
