from django.urls import path
from . import views
urlpatterns = [
    path('swaphouse/', views.index, name='swap_house.index'),
]