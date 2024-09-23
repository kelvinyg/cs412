from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
# Create your views here.

quotes = [
    'Worry more about what you want to do than what you want to be', 
    'Even when things are tough, dont lose respect for the other person', 
    'Hope is that thing inside us that insists, despite all the evidence to the contrary, that something better awaits us if we have the courage to reach for it, and to work for it, and to fight for it ']
images = ['quotes/barack-img/barack1.webp', 
        'quotes/barack-img/barack2.jpg', 
        'quotes/barack-img/barack3.jpg'
        ]

def quote(request):
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    
    context = {
        'quote' : random_quote,
        'image' : random_image
    }

    return render(request, "quotes/quote.html", context)

def show_all(request): 
    context = {
        'quotes' : quotes,
        'images' : images
    }
    return render(request, "quotes/show_all.html", context)


def about(request):
    template_name = "quotes/about.html"
    return render(request, template_name)