from django.urls import path
from . import views
urlpatterns = [
    path('marketplace/', views.index, name='marketplace.index'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('marketplace/listing/<int:id>/', views.listing_detail, name='listing_detail'),  # Listing details page

]