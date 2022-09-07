import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


def get_request(url, **kwargs):

    # If argument contain API KEY
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))

    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]

            # Basic authentication GET
            response = requests.get(
                url, 
                params=params, 
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key))

        else:
            # No authentication GET
            response = requests.get(
                url, 
                headers={'Content-Type': 'application/json'},
                params=kwargs)

    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    return json_data


def post_request(url, payload, **kwargs):

    try:
        response = requests.post(url, params=kwargs, json=payload)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):

    print('')
    print('==== get_dealers_from_cf: =========================================')

    results = []

    json_result = get_request(url)
#    print(json_result)
    print('')

    if json_result:
        dealers = json_result['body']
        for dealer in dealers:
            dealer_doc = dealer['doc']
            dealer_obj = CarDealer(
                address    = dealer_doc['address'], 
                city       = dealer_doc['city'], 
                full_name  = dealer_doc['full_name'],
                id         = dealer_doc['id'], 
                lat        = dealer_doc['lat'], 
                long       = dealer_doc['long'],
                short_name = dealer_doc['short_name'],
                st         = dealer_doc['st'], 
                state      = dealer_doc['state'], 
                zip        = dealer_doc['zip'])
            results.append(dealer_obj)

            print( dealer_obj )
    else:
        result = 'Unknown error'

    print('')
    return results


def get_dealer_by_id_from_cf(url, id):

    print('')
    print('==== get_dealer_by_id_from_cf: Dealership ID is : ' + str(id) + ' ===================')

    json_result = get_request(url, id=id)
#    print(json_result)
    print('')

    if json_result:
        dealer_doc = json_result['body'][0]
        dealer_obj = CarDealer(
            address    = dealer_doc['address'], 
            city       = dealer_doc['city'], 
            full_name  = dealer_doc['full_name'],
            id         = dealer_doc['id'], 
            lat        = dealer_doc['lat'], 
            long       = dealer_doc['long'],
            short_name = dealer_doc['short_name'],
            st         = dealer_doc['st'], 
            state      = dealer_doc['state'], 
            zip        = dealer_doc['zip'])
    else:
        result = 'Unknown error'

    print('')
    print( dealer_doc )

    print('')
    return dealer_obj


def get_dealers_by_st_from_cf(url, state):

    print('')
    print('==== get_dealers_by_st_from_cf: State is : ' + str(state) + ' ===================')

    json_result = get_request(url, st=state)
#    print(json_result)
    print('')

    results = []

    if json_result:
        dealers = json_result["body"]

        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

            print('')
            print( dealer_obj )
    else:
        result = 'Unknown error'

    print('')
    return results


def get_dealer_reviews_from_cf(url, **kwargs):

    id = kwargs.get("id")

    print('')
    print('==== get_dealer_reviews_from_cf: Dealership ID is : ' + str(id) + ' ===================')

    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
#    print(json_result)
    print('')

    results = []

    if json_result:

        reviews = json_result['body']['data']['docs']

        for review in reviews:

            review_obj = DealerReview(
                dealership    = review['dealership'],
                name          = review['name'],
                purchase      = review['purchase'],
                review        = review['review'],
                )

            if "id" in review:
                review_obj.id = review["id"]
            if "purchase_date" in review:
                review_obj.purchase_date = review["purchase_date"]
            if "make" in review:
                review_obj.make = review["make"]
            if "model" in review:
                review_obj.model = review["model"]
            if "year" in review:
                review_obj.year = review["year"]

            review_obj.sentiment = analyze_review_sentiments( review_obj.review )

            results.append(review_obj)

            print('')
            print(review)
    else:
        result = 'Unknown error'

    print('')
    return results


def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8c6a1c26-bfa8-4356-93a8-c2a86e861ad8"
    api_key = "RK2Pgz1pF7kOSZgLQSeQVG34FYOfwyq512cHVKD8rKQF"
    authenticator = IAMAuthenticator( api_key )
    natural_language_understanding = NaturalLanguageUnderstandingV1( version='2022-08-01',authenticator=authenticator )
    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(
        text = text+"hello hello hello",
        features = Features(
            sentiment = SentimentOptions(
                targets = [ text + "hello hello hello" ]))).get_result()

    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return(label)

