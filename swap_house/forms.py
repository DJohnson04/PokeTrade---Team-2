from django import forms
from accounts.models import UserPokemon

class PostTradeForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(
        queryset=UserPokemon.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select cards from your collection"
    )
    def __init__(self, *args, **kwargs):
        user_account = kwargs.pop('user_account')
        super().__init__(*args, **kwargs)
        # Only show cards NOT already in a listing/trade and owned by user
        qs = user_account.pokemons.filter(is_selling=False)
        self.fields['offered_cards'].queryset = qs

class OfferTradeForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(
        queryset=UserPokemon.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select cards you want to offer"
    )
    def __init__(self, *args, **kwargs):
        user_account = kwargs.pop('user_account')
        super().__init__(*args, **kwargs)
        qs = user_account.pokemons.filter(is_selling=False)
        self.fields['offered_cards'].queryset = qs
