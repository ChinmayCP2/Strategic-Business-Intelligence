# from django.http import JsonResponse
import os
import json
import logging
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import get_token
from dotenv import load_dotenv
from lgd.models import DistrictModel
from .models import JSONDataModel, DataModel, CatagoryModel
from .generate import generate_id, generate_primary_type
# Create your views here.
load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

@csrf_exempt
def send_json_response(request):
    '''Resource'''
    # csrf_token = get_token(request)
    # csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)
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
                      'googleMapsUri', 'businessStatus', 'userRatingCount', 
                      'stateCode', 'districtCode','subdistrictCode','vilageCode' ]

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
    
        # for element in neccessary_fields:
        #     # Checking if all fields are present if not setting them to Null
        #     if element not in place:
        #         place[element] = None
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
        # print(data)
        for place in data['places']: 
                # Iterating through the places   
            JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
            logging.info('JsonField Saved')
    # places = [JSONDataModel(place) for place in data['places']]
    
    places = JSONDataModel.objects.all() # pylint: disable=maybe-no-member   
    # print(places)
    for place in places:
        place_catagory, created = CatagoryModel.objects.get_or_create(catagory=str(place.jsonData.get('catagory'))) # pylint: disable=maybe-no-member
        DataModel.objects.get_or_create(id = place.jsonData.get("id"), # pylint: disable=maybe-no-member 
                                        name= place.jsonData.get('displayName').get('text'),  
                                        # catagory = place.jsonData.get('catagory'),
                                        catagory = place_catagory,                                    
                                        # primaryType = place.jsonData.get('primaryType'),
                                        formattedAddress = place.jsonData.get('formattedAddress'),
                                        locationLongitude = place.jsonData.get('location').get('longitude'),
                                        locationLatitude = place.jsonData.get('location').get('latitude'),
                                        rating = place.jsonData.get('rating'),
                                        # rating = None,
                                        googleMapsUri = place.jsonData.get('googleMapsUri'),
                                        businessStatus = place.jsonData.get('businessStatus'),
                                        userRatingCount = place.jsonData.get('userRatingCount'),
                                        stateCode = place.jsonData.get('stateCode'),
                                        districtCode = place.jsonData.get('districtCode'),
                                        subdistrictCode = place.jsonData.get('subdistrictCode'),
                                        villageCode = place.jsonData.get('villageCode'),
                                        # userRatingCount = None
                                        # accessibilityOptions = []
                                        )
    logging.info('Extracted Data from JSON')
    return HttpResponse("data inserted")
        
# def extract_json(request):
#     '''to store json data into the defined model'''
    
#     return HttpResponse("data saved")
    

