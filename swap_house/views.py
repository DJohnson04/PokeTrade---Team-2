from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'PokeTrade'
    return render(request, 'swap_house/index.html', {
        'template_data': template_data})