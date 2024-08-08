from celery import shared_task
from .models import JSONDataModel, DataModel, CatagoryModel, CountModel
from lgd.models import SubDistrictModel, VillageModel
# from .views import fetch_api_data, save_json, assign_category
from django.db.models import Count
from dotenv import load_dotenv
import logging
from django.http import JsonResponse
import requests
import os
import json

load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

@shared_task
def fetch_and_save_data(state, district):
    logging.info('Starting task')
    all_places = fetch_api_data(state, district)
    logging.info('fetch api done starting json save')
    places = save_json(all_places)
    logging.info('saving extracted data')
    assign_category(places)
    logging.info('counting')
    count_places_by_catagory(state,district)

def fetch_api_data(state,district):
    '''fetching data from the api for the given district'''
    # print(state, district)
    if not state or not district:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    all_places = []
    tasks = []
    subdistricts = SubDistrictModel.objects.filter(districtCode=district)  # pylint: disable=maybe-no-member
    for subdistrict in subdistricts:
                # Loop over villages 
        villages = VillageModel.objects.filter(subdistrictCode=subdistrict)  # pylint: disable=maybe-no-member
        for village in villages:
            village_payload = {
                "stateCode": state,
                "districtCode": district,
                "subdistrictCode": subdistrict.subdistrictCode,
                "villageCode": village.villageCode
            }
            tasks.append(village_payload)
            headers = {
                "Content-Type": "application/json"
            }
            # making a request to all villages for places data
            village_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload),
                                              headers=headers)
            if village_response.status_code == 200:
                village_places = village_response.json().get("places", [])
                # print(f"village_places: {village_places}")  # Debugging
                if isinstance(village_places, list):
                    for place in village_places:
                        # print(f"place: {place}, type: {type(place)}")  # Debugging
                        if isinstance(place, dict):
                            # adding location codes to the places returned by the api
                            place.update({'stateCode': state, 'districtCode': district,
                                          'subdistrictCode': subdistrict.subdistrictCode,
                                            'villageCode': village.villageCode})
                    all_places.extend(village_places)
                else:
                    return JsonResponse({'error': 'Invalid format for village places'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to get village places'}, status=500)
    return all_places

def save_json(all_places):
    '''saving data to JSONModel as API response'''
    JSONDataModel.objects.all().delete() # pylint: disable=maybe-no-member
    for place in all_places:
        JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
    places = JSONDataModel.objects.all().values("jsonData") # pylint: disable=maybe-no-member 
    return places

def assign_category(places):
    '''assigning catagory and extracting data into DataModel'''
    for place in places:
        data = place.get("jsonData")
        type_mapping = {
            'retail': ['shop', 'retail', 'mart', 'croma', 'oulet', 'store'],
            'food': ['food', 'restaurant', 'hotel', 'fastfood', ],
            'finance': ['Finance', 'solutions', 'consultant', 'planner'],
            'healthcare': ['healthcare', 'medical', 'labs', 'hospital','clinic'],
            'education': ['education', 'school', 'college', 'university', 'institute']
        }   
        if 'displayName' in data:
            display_name = str(data.get('displayName')).lower()
            place_catagory, created = CatagoryModel.objects.get_or_create(catagory="other") # pylint: disable=maybe-no-member

        # Iterate over the type mapping
        for catagory, keywords in type_mapping.items():
            for keyword in keywords:
                if keyword in display_name:
                    place_catagory, created = CatagoryModel.objects.get_or_create(catagory=catagory)  # pylint: disable=maybe-no-member
                    break
            if keyword in display_name:
                break
        DataModel.objects.get_or_create( name= data.get('displayName'),  # pylint: disable=maybe-no-member
                                        # catagory = place.jsonData.get('catagory'),
                                        catagory = place_catagory,                                    
                                        # primaryType = place.jsonData.get('primaryType'),
                                        formattedAddress = data.get('formattedAddress'),
                                        locationLongitude = data.get('location').get('lng'),
                                        locationLatitude = data.get('location').get('lat'),
                                        rating = data.get('rating'),
                                        # rating = None,
                                        googleMapsUri = data.get('googleMapsUri'),
                                        businessStatus = data.get('businessStatus'),
                                        userRatingCount = data.get('userRatingCount'),
                                        stateCode = data.get('stateCode'),
                                        districtCode = data.get('districtCode'),
                                        subdistrictCode = data.get('subdistrictCode'),
                                        villageCode = data.get('villageCode'),
                                        # userRatingCount = None
                                        # accessibilityOptions = []
                                        defaults={'id': data.get("uuid")}
                                        )

# def count_places_by_catagory(state,district):
#     '''The counting function'''
#     print("counting started")
#             # After creating/updating DataModel entries, perform the counting operation
#     annotated_data = DataModel.objects.values('stateCode', 'districtCode',
#                                               'subdistrictCode',
#                                               'villageCode', 'catagory').annotate(place_count=Count('id'))

#             # Iterate over the annotated data and update the CountModel
#     for data in annotated_data:
            
#             catagory_instance = CatagoryModel.objects.filter(pk=data['catagory']).first() 
#             place_count = data['place_count']
#             # print(catagory)
#             CountModel.objects.filter(stateCode=state,districtCode=district).update_or_create(
#                     stateCode=data.get('stateCode'),
#                     districtCode=data.get('districtCode'),
#                     subdistrictCode=data.get('subdistrictCode'),
#                     villageCode=data.get('villageCode'),
#                     catagory=catagory_instance,
#                     defaults={'count': place_count}
#                 )

def count_places_by_catagory(state, district):
    print("counting started")
    annotated_data = DataModel.objects.filter(stateCode=state, districtCode=district).values('catagory').annotate(place_count=Count('id'))

    for data in annotated_data:
        catagory_instance = CatagoryModel.objects.get(pk=data['catagory'])
        place_count = data['place_count']
        CountModel.objects.create(
            stateCode=state,
            districtCode=district,
            catagory=catagory_instance,
            count=place_count
        )

    