from django.urls import path
from . import views

app_name = 'swap_house'

urlpatterns = [
    path('', views.trade_list_view, name='index'),
    path('post/', views.post_trade_view, name='post_trade'),
    path('trades/', views.trade_list_view,  name='trade_list'),
    path('trades/<int:trade_id>/offer/', views.offer_trade_view, name='offer_trade'),
    path('trades/<int:trade_id>/', views.trade_detail_view, name='trade_detail'),
    path('trades/<int:trade_id>/offer/<int:offer_id>/accept/', views.accept_offer_view, name='accept_offer'),
    path('trades/<int:trade_id>/offer/<int:offer_id>/reject/', views.reject_offer_view, name='reject_offer'),
]
