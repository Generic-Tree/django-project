from django import forms

from lottery import models
from utils import widgets


class BetAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BetAdminForm, self).__init__(*args, **kwargs)

        self.fields['tournament'] = forms.ModelChoiceField(
            models.Tournament.objects.all(),
            initial=self.tournament,
            disabled=True,
        )

        self.fields['choices'] = forms.ModelMultipleChoiceField(
            models.Bettable.objects.filter(value__lte=self.tournament.range),
            widget=widgets.ColumnCheckboxSelectMultiple(self.tournament.range / 10),
        )

    def clean_choices(self):
        value = self.cleaned_data['choices']
        if len(value) > self.tournament.choices_limit:
            raise forms.ValidationError(f"You can't select more than {self.tournament.choices_limit} items.")
        return value

    class Meta:
        model = models.Bet
        fields = '__all__'

    @property
    def tournament(self):
        return getattr(self, '_tournament', None) or models.Tournament.objects.latest()

    @classmethod
    def from_tournament(cls, tournament):
        if tournament:
            return type(
                tournament.__class__.__name__ + str(tournament) + cls.__name__,
                (cls,),
                {'_tournament': tournament}
            )
        return cls
