from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime

from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealers_by_st_from_cf, get_dealer_reviews_from_cf, post_request

import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')

        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)

    else:
        return render(request, 'djangoapp/login.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}

    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)

    # If it is a POST request
    elif request.method == 'POST':

        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, log this as a new user
            logger.error("New user")

        # If it is a new user
        if not user_exist:

            # Create user in auth_user table
            user = User.objects.create_user(username=username, 
                first_name=first_name, last_name=last_name, password=password)

            # Login the user and redirect to home page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# To render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf( url )
        context["dealerships"] = dealerships

        return HttpResponse(dealerships)
#        return dealerships


def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}

        dealer_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf( dealer_url, id=id )
        context["dealer"] = dealer
    
        review_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf( review_url, id=id )
        context["reviews"] = reviews

        return HttpResponse(reviews)
#        return reviews


def add_review(request, id):
    if request.user.is_authenticated:

        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.user.first_name + " " + request.user.last_name
        review["dealership"] = id
        review["review"] = 'This is test review #4'
        review["purchase"] = True
        review["purchase_date"] = '2022, 1, 1'
        review["car_make"] = 'Ford'
        review["car_model"] = 'Escort'
        review["car_year"] = '2022'

        json_payload = { "review": review }
        url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/review"
        results = post_request( url, json_payload, id=id )

        print(results)
        return HttpResponse(results)
#        return results

