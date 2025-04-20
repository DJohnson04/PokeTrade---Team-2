from django.urls import path
from . import views
urlpatterns = [
    path('marketplace/', views.index, name='marketplace.index'),
]