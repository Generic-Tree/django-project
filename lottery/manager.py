from django.db.models import manager

from lottery import query


class TournamentManager(
    manager.Manager.from_queryset(query.TournamentQueryset)
):

    def get_queryset(self):
        return super(TournamentManager, self).get_queryset().prefetch_related('bets')  #\
            # .annotate_bet_count()
