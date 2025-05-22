# File: views.py
# Author: Becky Geisberg, (rgeis26@bu.edu)
# Description: views file for restaurants

from django.shortcuts import render
import time
import random

# Create your views here.
def order(request):
    '''Show the web page with the form.'''

    specials = [
        "Crimson Crumble",
        "Whisker Twist",
        "Lemon Moon Puffs",
        "The Velvet Swirl",
        "Maple Mirage",
        "Rose Quartz Tartlets",
        "ChocoLooms"
    ]

    index = random.randint(0, len(specials) - 1)
    daily_special = specials[index]
    context = {
        "daily_special" : daily_special
    }


    template_name = "restaurant/order.html"
    return render(request, template_name, context=context)
   

def main(request):
    """ main page display """
    template_name = "restaurant/main.html"
    image = 'images/bakery.jpg'
    context = {
        'image': image
    }
    return render(request, template_name, context=context)

def confirmation(request):
    '''Process the form submission, and generate a result.'''

    template_name = "restaurant/confirmation.html"

    # read the form data into python variables:
    if request.POST:

        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']

        special_instructions = request.POST.get('special_instructions', "none")
        daily_special = request.POST.get('daily_special', "not ordered")

        cheese_danish = request.POST.get('cheese_danish', "not ordered")
        warmed_danish = request.POST.get('cheese-yes-no', "no")

        cinnamon_twist = request.POST.get('cinnamon_twist', "not ordered")
        warmed_twist = request.POST.get('cinnamon-yes-no', 'no')

        chocolate_chip_muffin = request.POST.get('chocolate_chip_muffin', "not ordered")
        warmed_muffin = request.POST.get('muffin-yes-no', "no")

        fruit_tart = request.POST.get('fruit_tart', "not ordered")
        # Get current time in seconds since epoch
        current_seconds = time.time()

        # Generate random number of minutes (30 to 60), convert to seconds
        extra_seconds = random.randint(30, 60) * 60

        # Add to current time
        future_seconds = current_seconds + extra_seconds

        # Convert back to time string
        formatted = time.strftime("%H:%M:%S", time.localtime(future_seconds))
        

        context = {
            'name': name,
            'phone_number': phone_number,
            'email': email,
            "special_instructions": special_instructions,
            'daily_special': daily_special,
            'cheese_danish': cheese_danish,
            'warmed_danish': warmed_danish,
            'cinnamon_twist': cinnamon_twist,
            'warmed_twist':warmed_twist,
            'chocolate_chip_muffin': chocolate_chip_muffin,
            'warmed_muffin': warmed_muffin,
            'fruit_tart': fruit_tart, 
            'time': formatted,
        }

    return render(request, template_name, context=context)


