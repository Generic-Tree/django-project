from django.db import models
from django.db.models import signals, functions, aggregates

from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from lottery import manager
from utils import fields


__all__ = [
    'Tournament',
    'Bettable',
    'Bet'
]


class Tournament(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    start = fields.FutureDateTimeField(verbose_name=_('start'))
    range = models.IntegerField(verbose_name=_('range'))
    choices_limit = 7

    # bet_count = fields.RelationCountField('bets')

    # bet_count = fields.VirtualFunctionField(
    #     function=aggregates.Count('bets'),
    #     output_field=fields.IntegerField()
    # )

    @property
    def bet_count(self):
        return self.bets.count()
    # bet_count.fget.short_description = _('bet count')

    class Meta:
        verbose_name = _('Tournament')
        get_latest_by = 'id'

    objects = manager.TournamentManager()

    def __str__(self):
        return self.title


@receiver(signals.post_save, sender=Tournament, dispatch_uid="create_range")
def create_range(sender, instance, **kwargs):
    Bettable.objects.bulk_create([
        Bettable(value=value + 1)
        for value
        in range(instance.range)
    ], ignore_conflicts=True)


class Bettable(models.Model):
    value = models.IntegerField(verbose_name=_('value'), unique=True)

    class Meta:
        verbose_name = _('Bettable')
        ordering = ['value']

    def __str__(self):
        return str(self.value)

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.value > other.value
        return False


class Bet(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        related_name='bets',
        on_delete=models.CASCADE,
        verbose_name=_('Tournament'),
    )
    choices = models.ManyToManyField(
        Bettable,
        related_name='bet',
        related_query_name='bet',
        verbose_name=_('choices'),
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('registered at'),
    )

    @property
    def bet_choices(self):
        return [
            num.value
            for num
            in sorted(self.choices.all())
        ]
    bet_choices.fget.short_description = _('bet choices')

    @property
    def choices_limit(self):
        return self.tournament.choices_limit

    class Meta:
        verbose_name = _('Bet')
        ordering = ['-registered_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tournament', 'id'], name='bet_id'
            )
        ]

    def __str__(self):
        return ", ".join(
            str(value)
            for value in
            self.bet_choices
        )


# @receiver(signals.m2m_changed, sender=Bet.choices.through, dispatch_uid="create_range")
# def choices_changed(sender, instance, **kwargs):
#     if len(instance.choices.all()) >= instance.choices_limit:
#         raise ValidationError(f'Max number of records is {instance.choices_limit}')
