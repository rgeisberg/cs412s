from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
def home(request):
    '''fund to respond to the "home" request.'''
    responseText = f'''
    <html>
    <h1>Hello, world!</h1>
    The current time is {time.ctime()}
    </html>
    ''' 
    return HttpResponse(responseText)
def home_page(request):
    '''Respond to the URL, delegate work to a template'''
    template_name ='hw/home.html'
    #dictionary of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
    }
    return render(request, template_name,context )

def about(request):
    '''Respond to the URL 'about', delegate work to a template'''
    template_name ='hw/about.html'
    #dictionary of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
    }
    return render(request, template_name,context )

