from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

#if logged in, display cards gathered from database(currently the html is blank)
@login_required()
def index(request):
    template_data = {}
    template_data['title'] = 'collection'
    return render(request, 'collection/index.html', {
        'template_data': template_data})