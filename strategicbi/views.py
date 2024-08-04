import os
import json
import logging
import requests
import json
import random
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
# from django.middleware.csrf import get_token
from dotenv import load_dotenv
from .forms import LocationForm, RegistrationForm
from lgd.models import SubDistrictModel, StateModel, DistrictModel, VillageModel
# from utils.decorators import custom_permission_required
from .models import JSONDataModel, DataModel, CatagoryModel, CountModel
from .generate import generate_random_places
# Create your views here.
load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")

@csrf_exempt
def send_json_response(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            state_code = data.get('stateCode')
            district_code = data.get('districtCode')
            subdistrict_code = data.get('subdistrictCode')
            village_code = data.get('villageCode')

            if not state_code or not district_code:
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            places = []
            if village_code:
                # places = generate_random_places(random.randint(0, 1))
                pass
            elif subdistrict_code:
                # places = generate_random_places(random.randint(2, 4))
                pass
            elif district_code:
                places = generate_random_places(random.randint(4, 5))

            return JsonResponse({'places': places}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/login')
def home(request):
    '''index'''
    form = LocationForm(request.POST or None)
    context = {}
    if request.method == 'POST':   
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        catagoryChosen = data.get('catagory')
        # print(state, district)
        if not state or not district:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        all_places = []

        # Get district places
        payload = {
            "stateCode": state,
            "districtCode": district
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(payload), headers=headers)
        
        if response.status_code == 200:
            district_places = response.json().get("places")
            # print(f"district_places: {district_places}")  # Debugging
            if isinstance(district_places, list):
                for place in district_places:
                    # print(f"place: {place}, type: {type(place)}")  # Debugging
                    if isinstance(place, dict):
                        place.update({'stateCode': state, 'districtCode': district})
                all_places.extend(district_places)
            else:
                return JsonResponse({'error': 'Invalid format for district places'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to get district places'}, status=500)

        # Loop over subdistricts
        subdistricts = SubDistrictModel.objects.filter(districtCode=district)  # pylint: disable=maybe-no-member
        for subdistrict in subdistricts:
            subdistrict_payload = {
                "stateCode": state,
                "districtCode": district,
                "subdistrictCode": subdistrict.subdistrictCode
            }
            subdistrict_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(subdistrict_payload), headers=headers)
            if subdistrict_response.status_code == 200:
                subdistrict_places = subdistrict_response.json().get("places", [])
                # print(f"subdistrict_places: {subdistrict_places}")  # Debugging
                if isinstance(subdistrict_places, list):
                    for place in subdistrict_places:
                        # print(f"place: {place}, type: {type(place)}")  # Debugging
                        if isinstance(place, dict):
                            place.update({'stateCode': state, 'districtCode': district, 'subdistrictCode': subdistrict.subdistrictCode})
                    all_places.extend(subdistrict_places)

                    # Loop over villages
                    villages = VillageModel.objects.filter(subdistrictCode=subdistrict)  # pylint: disable=maybe-no-member
                    for village in villages:
                        village_payload = {
                            "stateCode": state,
                            "districtCode": district,
                            "subdistrictCode": subdistrict.subdistrictCode,
                            "villageCode": village.villageCode
                        }
                        village_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload), headers=headers)
                        if village_response.status_code == 200:
                            village_places = village_response.json().get("places", [])
                            # print(f"village_places: {village_places}")  # Debugging
                            if isinstance(village_places, list):
                                for place in village_places:
                                    # print(f"place: {place}, type: {type(place)}")  # Debugging
                                    if isinstance(place, dict):
                                        place.update({'stateCode': state, 'districtCode': district, 'subdistrictCode': subdistrict.subdistrictCode, 'villageCode': village.villageCode})
                                all_places.extend(village_places)
                            else:
                                return JsonResponse({'error': 'Invalid format for village places'}, status=500)
                        else:
                            return JsonResponse({'error': 'Failed to get village places'}, status=500)
                else:
                    return JsonResponse({'error': 'Invalid format for subdistrict places'}, status=500)
            else:
                return JsonResponse({'error': 'Failed to get subdistrict places'}, status=500)
        
        # place_catagory, created = CatagoryModel.objects.get_or_create(catagory=str(place.get('catagory'))) # pylint: disable=maybe-no-member
        # return JsonResponse({'places': all_places}, status=200)
        # saving json data directly into the tables
        JSONDataModel.objects.all().delete()
        for place in all_places:
            JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
            logging.info('JsonField Saved')
        places = JSONDataModel.objects.all().values("jsonData") # pylint: disable=maybe-no-member   
        # print(places)
        for place in places:
            data = place.get("jsonData")
            type_mapping = {
                'retail': ['shop', 'retail', 'mart', 'croma', 'oulet', 'store'],
                'food': ['food', 'restaurant', 'hotel', 'fastfood', ],
                'finance': ['Finance', 'solutions', 'consultant', 'planner'],
                'healthcare': ['healthcare', 'medical', 'labs', 'hospital','clinic']
            }
            
            if 'displayName' in data:
                display_name = str(data.get('displayName')).lower()
                place_catagory, created = CatagoryModel.objects.get_or_create(catagory="other")

            # Iterate over the type mapping
            for catagory, keywords in type_mapping.items():
                for keyword in keywords:
                    if keyword in display_name:
                        place_catagory, created = CatagoryModel.objects.get_or_create(catagory=catagory)  # pylint: disable=maybe-no-member
                        break
                if keyword in display_name:
                    break
            # print(place_catagory.id)
            # print(data)          
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
        # distinct_locations = DataModel.objects.only('stateCode','districtCode','subdistrictCode','villageCode','catagory').distinct() # pylint: disable=maybe-no-member
            print("counting started")
            # After creating/updating DataModel entries, perform the counting operation
            annotated_data = DataModel.objects.values('stateCode', 'districtCode', 'catagory').annotate(place_count=Count('id'))

                # Iterate over the annotated data and update the CountModel
            for data in annotated_data:
                state_code = data.get('stateCode')
                district_code = data.get('districtCode')
                catagory_instance = CatagoryModel.objects.filter(pk=data['catagory']).first() 
                place_count = data['place_count']
                # print(catagory)
                CountModel.objects.update_or_create(
                        stateCode=state_code,
                        districtCode=district_code,
                        catagory=catagory_instance,
                        defaults={'count': place_count}
                    )
        return HttpResponseRedirect(reverse('display_view'))

    context['form'] = form
    return render(request, 'frontend/home.html', context)

def display_view(request):
    distinct_locations = DataModel.objects.values('stateCode', 'districtCode').distinct() # pylint: disable=maybe-no-member
    updated_locations = []
    for location in distinct_locations:
        state_code = location.get("stateCode")
        district_code = location.get("districtCode")
        state_name = StateModel.objects.get(pk=state_code).stateNameEnglish # pylint: disable=maybe-no-member
        district_name = DistrictModel.objects.get(pk=district_code).districtNameEnglish # pylint: disable=maybe-no-member
         
        # Update the location dictionary with state and district names
        location.update({'state_name': state_name, 'district_name': district_name})
        
        # Add the updated location to the list
        updated_locations.append(location)
    # print(distinct_locations)
    context = {
        'distinct_locations': updated_locations,
    }
    return render(request, 'frontend/display.html', context)

def get_details(request):
    state_code = request.GET.get('stateCode')
    district_code = request.GET.get('districtCode')
    
    details = CountModel.objects.filter(stateCode=state_code, districtCode=district_code).values( # pylint: disable=maybe-no-member
        'stateCode', 'districtCode', 'catagory__catagory', 'count'
    )
    print(details)
    data = list(details)
    return JsonResponse(data, safe=False)       

    
def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form =  RegistrationForm()
    return render(request, "registration/signup.html", {"form" : form})


def load_districts(request):
    '''dropdown district'''
    state = request.GET.get('state')
    districts = DistrictModel.objects.filter(stateCode = state) # pylint: disable=maybe-no-member
    # print(districts)
    context = {'districts' : districts}
    return render(request, 'dropdown_options/district_options.html', context)

# def load_subdistricts(request):
#     '''dropdown of subdistrict'''
#     district_code = request.GET.get('district')
#     # print(district_code)
#     # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
#     # print(state)
#     subdistricts = SubDistrictModel.objects.filter(districtCode = district_code)# pylint: disable=maybe-no-member
#     # print(subdistricts)
#     context = {'subdistricts' : subdistricts}
#     return render(request, 'dropdown_options/subdistrict_options.html', context)

# def load_villages(request):
#     '''dropdown of subdistrict'''
#     subdistrict_code = request.GET.get('subdistrict')
#     print(subdistrict_code)
#     # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
#     # print(state)
#     villages = VillageModel.objects.filter(subdistrictCode = subdistrict_code)# pylint: disable=maybe-no-member
#     # print(villages)
#     context = {'villages' : villages}
#     return render(request, 'dropdown_options/village_options.html', context)






# @permission_required('frontend.lgd_access', login_url='/login')
# def get_json(request):
#     '''to get json data from the JSON response'''
#     try:
#         request_to_get_json_data = requests.post(os.getenv('CATEGORICAL_DATA'),
#                                             data=request.POST, timeout=1000) 
        
#     except TimeoutError: 
#         logging.error("Exception while getting the json data",exc_info=True)
#     if request_to_get_json_data.status_code == 200:
#         data = request_to_get_json_data.json()
#         # print(data)
#         for place in data['places']: 
#                 # Iterating through the places   
#             JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
#             logging.info('JsonField Saved')
#     # places = [JSONDataModel(place) for place in data['places']]
    
#     places = JSONDataModel.objects.all() # pylint: disable=maybe-no-member   
#     # print(places)
#     for place in places:
#         place_catagory, created = CatagoryModel.objects.get_or_create(catagory=str(place.jsonData.get('catagory'))) # pylint: disable=maybe-no-member
#         DataModel.objects.get_or_create( name= place.jsonData.get('displayName').get('text'),  # pylint: disable=maybe-no-member
#                                         # catagory = place.jsonData.get('catagory'),
#                                         catagory = place_catagory,                                    
#                                         # primaryType = place.jsonData.get('primaryType'),
#                                         formattedAddress = place.jsonData.get('formattedAddress'),
#                                         locationLongitude = place.jsonData.get('location').get('longitude'),
#                                         locationLatitude = place.jsonData.get('location').get('latitude'),
#                                         rating = place.jsonData.get('rating'),
#                                         # rating = None,
#                                         googleMapsUri = place.jsonData.get('googleMapsUri'),
#                                         businessStatus = place.jsonData.get('businessStatus'),
#                                         userRatingCount = place.jsonData.get('userRatingCount'),
#                                         stateCode = place.jsonData.get('stateCode'),
#                                         districtCode = place.jsonData.get('districtCode'),
#                                         subdistrictCode = place.jsonData.get('subdistrictCode'),
#                                         villageCode = place.jsonData.get('villageCode'),
#                                         # userRatingCount = None
#                                         # accessibilityOptions = []
#                                         defaults={'id': place.jsonData.get("id")}
#                                         )

#     distinct_locations = DataModel.objects.only('stateCode','districtCode','subdistrictCode','villageCode','catagory').distinct() # pylint: disable=maybe-no-member
#     for location in distinct_locations:
#         place_count = DataModel.objects.filter(stateCode=location.stateCode, # pylint: disable=maybe-no-member
#                                                districtCode = location.districtCode,
#                                                subdistrictCode = location.subdistrictCode,
#                                                villageCode = location.villageCode,
#                                                catagory = location.catagory).count()
#         CountModel.objects.get_or_create(stateCode=location.stateCode, # pylint: disable=maybe-no-member
#                                          catagory = location.catagory, 
#                                          districtCode = location.districtCode,
#                                          subdistrictCode = location.subdistrictCode,
#                                          villageCode = location.villageCode,
#                                          count = place_count)
    # logging.info('Place count in village saved')
    # logging.info('Extracted Data from JSON')
    # return HttpResponse("data inserted")
        
# def extract_json(request):
#     '''to store json data into the defined model'''
    
#     return HttpResponse("data saved")
    

