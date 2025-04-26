from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import Listing, UserAccount
from collection.models import Pokemon
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Listing, UserAccount, UserPokemon
from .forms import ListingForm, ListingEditForm
from django.shortcuts import render, get_object_or_404
from accounts.models import Listing
from django.shortcuts import render
from django.db.models import F
from django.core.paginator import Paginator
from django.urls import reverse


@login_required()
def index(request):
    # Get all listings that are not sold
    listings = Listing.objects.filter(is_sold=False)

    # find user listings only
    if request.GET.get('my_listings'):
        listings = listings.filter(seller=request.user.useraccount)

    # Handle sorting by price
    sort_option = request.GET.get('sort_by', 'price_asc')
    if sort_option == 'price_asc':
        listings = listings.order_by('price')
    elif sort_option == 'price_desc':
        listings = listings.order_by('-price')

    # Paginate the listings
    paginator = Paginator(listings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for listing in listings:
        user_pokemon = listing.user_pokemon
        if not user_pokemon.is_selling:
            user_pokemon.is_selling = True
            user_pokemon.save()
    return render(request, 'marketplace/index.html', {
        'page_obj': page_obj,
        'sort_option': sort_option,
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
                is_sold=False,
            )
            user_pokemon.is_selling = True
            user_pokemon.save()
            return redirect('marketplace.index')
    else:
        form = ListingForm(user=request.user)
    for listing in Listing.objects.all():
        print(f"Listing ID: {listing.id}")
        print(f"Seller: {listing.seller.user.username}")
        print(f"Pokemon: {listing.user_pokemon.pokemon.name}")
        print(f"Price: {listing.price}")
        print(f"Is Sold: {listing.is_sold}")
        print(f"Created At: {listing.created_at}")
        print("------")
    return render(request, 'marketplace/create_listing.html', {'form': form})


def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})
def purchase_listing(request, id):
    buyer_account = UserAccount.objects.get(user=request.user)
    listing = get_object_or_404(Listing, id=id)

    if listing.seller == buyer_account:
        messages.error(request, "You can't buy your own listing.")
        return redirect('listing_detail', id=id)

    if buyer_account.wallet < listing.price:
        messages.error(request, "You don't have enough funds to buy this Pokémon.")
        return redirect('listing_detail', id=id)

    seller_account = listing.seller
    user_pokemon = listing.user_pokemon

    buyer_account.wallet -= listing.price
    seller_account.wallet += listing.price

    user_pokemon.owner = buyer_account
    user_pokemon.is_selling = False
    listing.is_sold = True

    buyer_account.save()
    seller_account.save()
    user_pokemon.save()
    listing.save()
    listing.delete()
    messages.success(request, f"You bought {user_pokemon.pokemon.name}!")
    return redirect('marketplace.index')



@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    if listing.seller.user != request.user:
        return redirect('marketplace.index')

    if request.method == 'POST':
        form = ListingEditForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('marketplace.index')  #
    else:
        form = ListingEditForm(instance=listing)

    return render(request, 'marketplace/edit_listing.html', {
        'form': form,
        'listing': listing,
    })
