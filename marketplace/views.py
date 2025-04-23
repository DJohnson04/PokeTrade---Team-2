from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Listing, UserAccount
from collection.models import Pokemon
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Listing, UserAccount, UserPokemon
from .forms import ListingForm
from django.shortcuts import render, get_object_or_404
from accounts.models import Listing

@login_required()
def index(request):
    # Retrieve all active listings from the marketplace
    listings = Listing.objects.filter(is_sold=False)  # Assuming only unsold listings should be shown

    # Pass listings to the template
    return render(request, 'marketplace/index.html', {
        'listings': listings
    })




@login_required
def create_listing(request):
    user_profile = UserAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form = ListingForm(user=request.user, data=request.POST)
        if form.is_valid():
            user_pokemon = form.cleaned_data['user_pokemon']
            price = form.cleaned_data['price']

            # Create a new Listing
            Listing.objects.create(
                seller=user_profile,
                user_pokemon=user_pokemon,
                price=price,
                is_sold=False
            )
            return redirect('marketplace.index')
    else:
        form = ListingForm(user=request.user)

    return render(request, 'marketplace/create_listing.html', {'form': form})


def listing_detail(request, id):
    # Get the listing by its ID, or return a 404 if it doesn't exist
    listing = get_object_or_404(Listing, id=id)

    # Pass the listing to the template
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})
