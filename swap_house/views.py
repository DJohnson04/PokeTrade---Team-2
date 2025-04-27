from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
import requests
from .models import Trade, TradeOffer
from .forms import PostTradeForm, OfferTradeForm
from accounts.models import UserAccount

@login_required
def index(request):
    return redirect('swap_house:trade_list')


@login_required
def post_trade_view(request):
    account, _ = UserAccount.objects.get_or_create(user=request.user)
    form = PostTradeForm(request.POST or None, user_account=account)

    if request.method == 'POST' and form.is_valid():
        trade = Trade.objects.create(poster=account)
        trade.offered_cards.set(form.cleaned_data['offered_cards'])
        trade.save()
        form.cleaned_data['offered_cards'].update(is_selling=True)
        return redirect('swap_house:trade_list')

    return render(request, 'swap_house/post_trade.html', {
        'template_data': {'title': 'Post Trade'},
        'form': form
    })


@login_required
def trade_list_view(request):
    open_trades = Trade.objects.filter(is_open=True)
    return render(request, 'swap_house/trade_list.html', {
        'template_data': {
            'title': 'Available Trades',
            'open_trades': open_trades
        }
    })


@login_required
def offer_trade_view(request, trade_id):
    trade = get_object_or_404(Trade, pk=trade_id, is_open=True)
    account, _ = UserAccount.objects.get_or_create(user=request.user)

    if trade.poster == account:
        return redirect('swap_house:trade_list')

    form = OfferTradeForm(request.POST or None, user_account=account)
    if request.method == 'POST' and form.is_valid():
        offer = TradeOffer.objects.create(trade=trade, offerer=account)
        offer.offered_cards.set(form.cleaned_data['offered_cards'])
        offer.save()
        form.cleaned_data['offered_cards'].update(is_selling=True)
        return redirect('swap_house:index')

    cards_data = []
    for card in trade.offered_cards.all():
        url = f"https://pokeapi.co/api/v2/pokemon/{card.pokemon.name.lower()}/"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            stats = data.get("stats", [])
        else:
            stats = []
        cards_data.append({
            "card": card,
            "stats": stats
        })

    return render(request, 'swap_house/trade_offer.html', {
    'template_data': {'title': 'Make an Offer'},
    'trade': trade,
    'form': form,
    'cards_data': cards_data,
    })



@login_required
def trade_detail_view(request, trade_id):
    account, _ = UserAccount.objects.get_or_create(user=request.user)
    trade = get_object_or_404(Trade, pk=trade_id, poster=account)
    offers = trade.offers.exclude(status__in=['rejected', 'cancelled'])
    return render(request, 'swap_house/trade_detail.html', {
        'template_data': {'title': 'Trade Details'},
        'trade': trade,
        'offers': offers
    })


@login_required
@transaction.atomic
def accept_offer_view(request, trade_id, offer_id):
    account, _ = UserAccount.objects.get_or_create(user=request.user)
    trade = get_object_or_404(Trade, pk=trade_id, poster=account, is_open=True)
    offer = get_object_or_404(TradeOffer, pk=offer_id, trade=trade, status='pending')

    for card in trade.offered_cards.all():
        card.owner = offer.offerer
        card.is_selling = False
        card.save()
    for card in offer.offered_cards.all():
        card.owner = account
        card.is_selling = False
        card.save()

    trade.is_open = False
    trade.save()
    offer.status = 'accepted'
    offer.save()
    trade.offers.filter(status='pending').update(status='rejected')

    return redirect('swap_house:received_offers')



@login_required
def reject_offer_view(request, trade_id, offer_id):
    account, _ = UserAccount.objects.get_or_create(user=request.user)
    trade = get_object_or_404(Trade, pk=trade_id, poster=account, is_open=True)
    offer = get_object_or_404(TradeOffer, pk=offer_id, trade=trade, status='pending')
    offer.status = 'rejected'
    offer.save()
    offer.offered_cards.update(is_selling=False)
    return redirect('swap_house:received_offers')


@login_required
def received_offers_view(request):
    account, _ = UserAccount.objects.get_or_create(user=request.user)
    # All offers on trades you’ve posted, excluding cancelled
    offers = TradeOffer.objects.filter(trade__poster=account) \
                               .exclude(status='cancelled')
    return render(request, 'swap_house/received_offers.html', {
        'template_data': {'title': 'Offers Received'},
        'received_offers': offers
    })
