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
        url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf( url )

#        return HttpResponse(dealerships)

        context = {}
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, id):
    if request.method == "GET":

        dealer_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf( dealer_url, id=id )
    
        review_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf( review_url, id=id )

#        return HttpResponse(reviews)

        context = {}
        context["dealer"] = dealer
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, id):

    dealer_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)

    context = {}
    context["dealer"] = dealer

    if request.method == 'GET':

        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':

        if request.user.is_authenticated:

            username = request.user.username

            print(request.POST)

            payload = dict()

            car_id = request.POST["car"]

            car = CarModel.objects.get(pk=car_id)

            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False

            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True

            payload["purchase_date"] = request.POST["purchasedate"]
            payload["make"] = car.make.name
            payload["model"] = car.name
            payload["year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload

            review_post_url = "https://c976d4c3.us-south.apigw.appdomain.cloud/api/review"
            results = post_request( review_post_url, new_payload, id=id )
            print(results)

#        return HttpResponse(results)

            return redirect("djangoapp:dealer_details", id=id)

