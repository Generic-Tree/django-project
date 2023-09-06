from django.db import models
from django.db.models import Count

from utils import decorators


class _QuerySet(models.QuerySet):

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class TournamentQueryset(_QuerySet):

    def annotate_bet_count(self):
        return self.annotate(bet_count=Count('bets'))

    @decorators.safe
    def from_request(self, request):
        if pk := request.GET.get('tournament'):
            return self.get(pk=pk)
        return None
