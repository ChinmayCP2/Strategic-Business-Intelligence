import os
import json
import logging
import requests
import datetime
from celery import shared_task
from django.http import JsonResponse
from django.db.models import Count
from dotenv import load_dotenv
from lgd.models import SubDistrictModel, VillageModel
from .models import JSONDataModel, DataModel, CatagoryModel, CountModel, SummeryModel

load_dotenv()
logger = logging.getLogger('strategicbi')

@shared_task
def fetch_and_save_data(state, district):
    '''fetching and save data function'''
    # user = User.objects.get(id=user_id)
    # district_status = SummeryModel.objects.filter(stateCode = state, # pylint: disable=maybe-no-member
    #                                               districtCode = district) 
    # # completed_phase = PhaseModel.objects.filter(phase = "Completed").first() # pylint: disable=maybe-no-member
    # # incomplete_status = district_status.exclude(phase=completed_phase)
    # # print(incomplete_status.values('district_name','phase_id'))
    # if not district_status.exists():
        # cache.set(f'task_status_{user_id}', 'Your task has been accepted!', timeout=3600)
    logger.info('Starting task') 
    all_places = fetch_api_data(state, district)
    SummeryModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
                                            districtCode=district) \
                            .update(fetch_status = "Completed",
                                    extraction_status = "In-Progress",
                                    aggrigation_status = "Not Started",
                                    fetch_end_time = datetime.datetime.now(), 
                                    extraction_start_time = datetime.datetime.now()
                                    )
    print(all_places)
    logger.info('fetch api done starting json save')
    places = save_json(all_places)
    logger.info('saving extracted data')
    assign_category(places)
    SummeryModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
                                            districtCode=district) \
                            .update(fetch_status = "Completed",
                                    extraction_status = "Completed",
                                    aggrigation_status = "In-Progress",
                                    extraction_end_time = datetime.datetime.now(),
                                    aggrigation_start_time = datetime.datetime.now()
                                    )
    print(places)
    logger.info('counting')
    count_places_by_catagory(state,district)
    SummeryModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
                                            districtCode=district) \
                            .update(fetch_status = "Completed",
                                    extraction_status = "Completed",
                                    aggrigation_status = "Completed",
                                    aggrigation_end_time = datetime.datetime.now()
                                    )            
    # message = "The Processing for the requested data has begun..."
    return True
    # return False


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
            # logger.info("sending request to send_data for village %s", village)
            try:
                village_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload),
                                                headers=headers)
            except requests.exceptions.Timeout:
                # print("Timed out")
                logger.error("Time out",exc_info=True)
                
            if village_response.status_code == 200:
                # logger.info('%s village request status 200',village)
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
                    # logger.info('village data saved')
                else:
                    logger.error('Invalid format for village places')
                    return JsonResponse({'error': 'Invalid format for village places'}, status=500)
            else:
                logger.error('Failed to get village places')
                return JsonResponse({'error': 'Failed to get village places'}, status=500)
    # print(village_places)
    return all_places

def save_json(all_places):
    '''saving data to JSONModel as API response'''
    JSONDataModel.objects.all().delete() # pylint: disable=maybe-no-member
    # logger.info('deleted privious json')
    for place in all_places:
        JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
    places = JSONDataModel.objects.all().values("jsonData") # pylint: disable=maybe-no-member 
    # logger.info('json Data saved')
    return places

def assign_category(places):
    '''assigning catagory and extracting data into DataModel'''
    place_catagory = CatagoryModel.objects.get_or_create(catagory='other') # pylint: disable=maybe-no-member 
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
            
        # Iterate over the type mapping
        for catagory, keywords in type_mapping.items():
            for keyword in keywords:
                if keyword in display_name:
                    place_catagory, created = CatagoryModel.objects.get_or_create(catagory=catagory, # pylint: disable=maybe-no-member
                                                                                   subCatagory = keyword)
                    # print(place_catagory)
                    logger.info("category according to %s keyword found or created", keyword)
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
        # logger.info("place data saved")

def count_places_by_catagory(state, district):
    '''count function'''
    print("counting started")
    annotated_data = DataModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
                                               districtCode=district).values('catagory'). \
                                                annotate(place_count=Count('id'))
    # logger.info("annoted data for states and districts saved")
    for data in annotated_data:
        catagory_instance = CatagoryModel.objects.get(pk=data['catagory']) # pylint: disable=maybe-no-member
        place_count = data['place_count']
        CountModel.objects.create(  # pylint: disable=maybe-no-member
            stateCode=state,
            districtCode=district,
            catagory=catagory_instance,
            count=place_count
        )
    # logger.info("count data saved")

    