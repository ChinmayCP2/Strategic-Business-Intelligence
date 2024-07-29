# from django.http import JsonResponse
import os
import requests
import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .models import JSONDataModel, DataModel
from .generate import generate_id, generate_primary_type
# Create your views here.
load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

@csrf_exempt
def send_json_response(request):
    '''Resource'''
    try:
        with open(os.getenv('JSON_FILE'), encoding="utf-8") as json_file:
            data = json.load(json_file)
        # json_file = open(os.getenv('JSON_FILE'), encoding="utf-8")
    except FileNotFoundError:
        logging.error("File not found")
        return HttpResponse('File not found')
    # deleting unnecessary fields
    unnecessary_fields = ['utcOffsetMinutes', 'adrFormatAddress', 'iconBackgroundColor',
                   'iconMaskBaseUri', 'internationalPhoneNumber', 'primaryTypeDisplayName',
                     'addressComponents', 'shortFormattedAddress','photos', 'internationalPhoneNumber']
    neccessary_fields = ['places', 'displayName', 'primaryType', 
                      'formattedAddress', 'location', 'rating', 
                      'googleMapsUri', 'businessStatus', 'userRatingCount'];

    for place in data['places']:
        for element in unnecessary_fields:
                # Checking if all fields are present for deleting
                try: 
                    del place[element]
                except KeyError:
                    pass 
        generate_id(place)
        generate_primary_type(place)
        # Iterating through the places
    
        for element in neccessary_fields:
            # Checking if all fields are present if not setting them to Null
            if element not in place:
                place[element] = None
    return JsonResponse(data , status=200)


def get_json(request):
    '''to get json data from the JSON response'''
    try:
        request_to_get_json_data = requests.post(os.getenv('CATEGORICAL_DATA'),
                                            data=request.POST, timeout=1000) 
    except TimeoutError: 
        logging.error("Exception while getting the json data",exc_info=True)
    if request_to_get_json_data.status_code == 200:
        data = request_to_get_json_data.json()
        print(data)
        for place in data['places']: 
                # Iterating through the places   
            JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
            logging.info('JsonField Saved')
    # places = [JSONDataModel(place) for place in data['places']]
    
    # print(places)
    # with open('temp.json', 'w', encoding="utf-8") as f:
    #     json.dump(data, f)
    return HttpResponse("data inserted")
        
def extract_json(request):
    '''to store json data into the defined model'''
    places = JSONDataModel.objects.all() # pylint: disable=maybe-no-member   
    # print(places)
    for place in places:       
        DataModel.objects.get_or_create(id = place.jsonData['id'], # pylint: disable=maybe-no-member 
                                        name= place.jsonData['displayName']['text'],  
                                        catagory = place.jsonData['primaryType'],
                                        formattedAddress = place.jsonData['formattedAddress'],
                                        locationLongitude = place.jsonData['location']['longitude'],
                                        locationLatitude = place.jsonData['location']['latitude'],
                                        rating = place.jsonData['rating'],
                                        # rating = None,
                                        googleMapsUri = place.jsonData['googleMapsUri'],
                                        businessStatus = place.jsonData['businessStatus'],
                                        userRatingCount = place.jsonData['userRatingCount'],

                                        # userRatingCount = None
                                        # accessibilityOptions = []
                                        )
    logging.info('Extracted Data from JSON')
    return HttpResponse("data saved")
    

