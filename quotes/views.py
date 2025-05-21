from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
quotes = ["You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.",
           "Unless someone like you cares a whole awful lot, nothing is going to get better. It's not.",
           "From there to here, from here to there, funny things are everywhere."
           ]
image_urls = ["images/oh_the_places_youll_go.jpg",
              "images/lorax.jpg",
              "images/one_fish_two_fish.jpg",
              "images/Dr_suess.jpg"               
            ]

def about(request):
    '''Respond to the URL 'about', delegate work to a template'''
    template_name ='quotes/about.html'
    #dictionary of context variables
    context = {
        "image": "images/Dr_suess.jpg"
    }
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL 'show_all', delegate work to a template'''
    template_name ='quotes/show_all.html'
    #dictionary of context variables
    all_quotes_images = zip(quotes, image_urls)
    return render(request, template_name, {'all_quotes_images': all_quotes_images})


def quote(request):
    '''Respond to the URL 'quote', delegate work to a template'''
    template_name ='quotes/quote.html'
    #dictionary of context variables
    index = random.randint(0, len(quotes) - 1)
    random_quote = quotes[index]
    random_image = image_urls[index]
    context = {
       "quote": random_quote,
       "image": random_image,
    }
    return render(request, template_name,context)




