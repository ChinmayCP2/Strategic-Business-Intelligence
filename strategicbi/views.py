# from django.http import JsonResponse
import os
import json
import logging
import requests
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
# from django.middleware.csrf import get_token
from dotenv import load_dotenv
# from lgd.models import DistrictModel
# from utils.decorators import custom_permission_required
from .models import JSONDataModel, DataModel, CatagoryModel, CountModel
from .generate import generate_id, generate_primary_type
# Create your views here.
load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")


@csrf_exempt
# @permission_required('frontend.lgd_access', login_url=None)
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
        # neccessary_fields = ['places', 'displayName', 'primaryType',
        #                   'formattedAddress', 'location', 'rating', 
        #                   'googleMapsUri', 'businessStatus', 'userRatingCount', 
        #                   'stateCode', 'districtCode','subdistrictCode','vilageCode' ]

    for place in data['places']:
        for element in unnecessary_fields:
                    # Checking if all fields are present for deleting
                try: 
                    del place[element]
                except KeyError:
                        pass
        generate_id(place)
        generate_primary_type(place)
    return JsonResponse(data , status=200)

@permission_required('frontend.lgd_access', login_url='/login')
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
        DataModel.objects.get_or_create( name= place.jsonData.get('displayName').get('text'),  # pylint: disable=maybe-no-member
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
                                        defaults={'id': place.jsonData.get("id")}
                                        )
    # counting places in states
    states = DataModel.objects.only('stateCode', 'catagory').distinct() # pylint: disable=maybe-no-member
    for state in states:
        place_count = DataModel.objects.filter(stateCode=state.stateCode, catagory= state.catagory).count() # pylint: disable=maybe-no-member
        CountModel.objects.get_or_create(stateCode=state.stateCode, # pylint: disable=maybe-no-member
                                         catagory = state.catagory, 
                                         districtCode = None,
                                         subdistrictCode = None,
                                         villageCode = None,
                                         count = place_count)
    logging.info('Place count in states saved')
    # counting places in districts
    # districts = DataModel.objects.only('stateCode','districtCode','catagory').distinct() # pylint: disable=maybe-no-member
    # for district in districts:
    #     place_count = DataModel.objects.filter(Q(stateCode=district.stateCode, # pylint: disable=maybe-no-member
    #                                            districtCode = district.districtCode,
    #                                            catagory = district.catagory) & ~Q(districtCode__isnull=True)).count() 
    #     CountModel.objects.get_or_create(stateCode=district.stateCode, # pylint: disable=maybe-no-member
    #                                      catagory = district.catagory, 
    #                                      districtCode = district.districtCode,
    #                                      subdistrictCode = None,
    #                                      villageCode = None,
    #                                      count = place_count)
    # logging.info('Place count in district saved')
    # # counnting places in subdistricts
    # subdistricts = DataModel.objects.only('stateCode','districtCode','subdistrictCode','catagory').distinct() # pylint: disable=maybe-no-member
    # for subdistrict in subdistricts:
    #     place_count = DataModel.objects.filter(Q(stateCode=subdistrict.stateCode, # pylint: disable=maybe-no-member
    #                                            districtCode = subdistrict.districtCode,
    #                                            subdistrictCode = subdistrict.subdistrictCode,
    #                                            catagory = subdistrict.catagory) &
    #                                              ~Q(districtCode__isnull=True,
    #                                                 subdistrictCode__isnull=True)).count() 
    #     CountModel.objects.get_or_create(stateCode=subdistrict.stateCode, # pylint: disable=maybe-no-member
    #                                      catagory = subdistrict.catagory, 
    #                                      districtCode = subdistrict.districtCode,
    #                                      subdistrictCode = subdistrict.subdistrictCode,
    #                                      villageCode = None,
    #                                      count = place_count)
    # logging.info('Place count in subdistrict saved')
    # # counnting places in villages
    # villages = DataModel.objects.only('stateCode','districtCode','subdistrictCode','villageCode','catagory').distinct() # pylint: disable=maybe-no-member
    # for village in villages:
    #     place_count = DataModel.objects.filter(Q(stateCode=village.stateCode, # pylint: disable=maybe-no-member
    #                                            districtCode = village.districtCode,
    #                                            subdistrictCode = village.subdistrictCode,
    #                                            villageCode = village.villageCode,
    #                                            catagory = village.catagory) &
    #                                              ~Q(districtCode__isnull=True,
    #                                                 subdistrictCode__isnull=True,
    #                                                 villageCode__isnull=True)).count()
    #     CountModel.objects.get_or_create(stateCode=village.stateCode, # pylint: disable=maybe-no-member
    #                                      catagory = village.catagory, 
    #                                      districtCode = village.districtCode,
    #                                      subdistrictCode = village.subdistrictCode,
    #                                      villageCode = village.villageCode,
    #                                      count = place_count)
    # logging.info('Place count in village saved')
    # counnting places in villages
    villages = DataModel.objects.only('stateCode','districtCode','subdistrictCode','villageCode','catagory').distinct() # pylint: disable=maybe-no-member
    for village in villages:
        place_count = DataModel.objects.filter(stateCode=village.stateCode, # pylint: disable=maybe-no-member
                                               districtCode = village.districtCode,
                                               subdistrictCode = village.subdistrictCode,
                                               villageCode = village.villageCode,
                                               catagory = village.catagory).count()
        CountModel.objects.get_or_create(stateCode=village.stateCode, # pylint: disable=maybe-no-member
                                         catagory = village.catagory, 
                                         districtCode = village.districtCode,
                                         subdistrictCode = village.subdistrictCode,
                                         villageCode = village.villageCode,
                                         count = place_count)
    logging.info('Place count in village saved')
    logging.info('Extracted Data from JSON')
    return HttpResponse("data inserted")
        
# def extract_json(request):
#     '''to store json data into the defined model'''
    
#     return HttpResponse("data saved")
    

