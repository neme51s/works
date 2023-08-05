from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def homePageView(request):
    return render(request, 'home.html')

class HomePageView(TemplateView):
    template_name = 'home.html'