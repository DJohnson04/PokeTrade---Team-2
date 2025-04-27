from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import UserAccount, UserPokemon

User = get_user_model()

class Trade(models.Model):
    poster = models.ForeignKey(UserAccount,
                               on_delete=models.CASCADE,
                               related_name='posted_trades')
    offered_cards = models.ManyToManyField(UserPokemon,
                                           related_name='trade_offers_in')
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"Trade #{self.id} by {self.poster.user.username}"

class TradeOffer(models.Model):
    trade = models.ForeignKey(Trade,
                              on_delete=models.CASCADE,
                              related_name='offers')
    offerer = models.ForeignKey(UserAccount,
                                on_delete=models.CASCADE,
                                related_name='made_offers')
    offered_cards = models.ManyToManyField(UserPokemon,
                                           related_name='offers_made')
    status = models.CharField(max_length=10, choices=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('cancelled','Cancelled'),
    ], default='pending')

    def __str__(self):
        return f"Offer #{self.id} on Trade #{self.trade.id}"
