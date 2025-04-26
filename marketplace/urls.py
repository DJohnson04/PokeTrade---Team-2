from django.urls import path
from . import views

urlpatterns = [
    path('marketplace/', views.index, name='marketplace.index'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('marketplace/listing/<int:id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:id>/buy/', views.purchase_listing, name='marketplace.purchase_listing'),
    path('marketplace/listing/<int:id>/edit/', views.edit_listing, name='edit_listing'),
]
