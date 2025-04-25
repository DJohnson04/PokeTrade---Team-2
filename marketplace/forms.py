from django import forms
from collection.models import Pokemon
from accounts.models import Listing, UserAccount, UserPokemon

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['user_pokemon', 'price']

    user_pokemon = forms.ModelChoiceField(queryset=None, label='Select Pokémon')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_pokemon'].queryset = UserPokemon.objects.filter(owner__user=user)
class ListingEditForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price