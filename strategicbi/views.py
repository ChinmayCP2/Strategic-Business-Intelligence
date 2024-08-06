import os
import json
import logging
import requests
import json
import random
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.decorators import permission_required
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

@login_required(login_url='/login')
def home(request):
    '''Home view'''
    form = LocationForm(request.POST or None)
    context = {}
    if 'catagory' in request.session:
            del request.session['catagory']
    if request.method == 'POST':   
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        request.session['catagory'] = data.get('catagory')

        return HttpResponseRedirect(reverse('display'))
    context['form'] = form
    return render(request, 'frontend/fetch.html', context)


@csrf_exempt
def send_json_response(request):
    '''dummy source'''
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
                '''sending data for all the villages'''
                places = generate_random_places(random.randint(0, 1))
            # elif subdistrict_code:
            #     places = generate_random_places(random.randint(2, 4))
            #     pass
            # elif district_code:
            #     places = generate_random_places(random.randint(4, 5))

            return JsonResponse({'places': places}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/login')
def fetch(request):
    '''fetch view'''
    form = LocationForm(request.POST or None)
    context = {}
    # deleting the previous catagory used by the user we we can set a new one when searching 
    if 'catagory' in request.session:
            del request.session['catagory']
    if request.method == 'POST':
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        # setting the category for displaying count
        request.session['catagory'] = data.get('catagory')
        all_places = fetch_api_data(state, district)
        places = save_json(all_places)
        assign_category(places)
        count_places_by_catagory()
        # print(state, district)
        # if not state or not district:
        #     return JsonResponse({'error': 'Missing required parameters'}, status=400)
        # all_places = []
        # subdistricts = SubDistrictModel.objects.filter(districtCode=district)  # pylint: disable=maybe-no-member
        # for subdistrict in subdistricts:
        #             # Loop over villages 
        #             villages = VillageModel.objects.filter(subdistrictCode=subdistrict)  # pylint: disable=maybe-no-member
        #             for village in villages:
        #                 village_payload = {
        #                     "stateCode": state,
        #                     "districtCode": district,
        #                     "subdistrictCode": subdistrict.subdistrictCode,
        #                     "villageCode": village.villageCode
        #                 }
        #                 headers = {
        #                     "Content-Type": "application/json"
        #                 }
        #                 # making a request to all villages for places data
        #                 village_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload), headers=headers)
        #                 if village_response.status_code == 200:
        #                     village_places = village_response.json().get("places", [])
        #                     # print(f"village_places: {village_places}")  # Debugging
        #                     if isinstance(village_places, list):
        #                         for place in village_places:
        #                             # print(f"place: {place}, type: {type(place)}")  # Debugging
        #                             if isinstance(place, dict):
        #                                 # adding location codes to the places returned by the api
        #                                 place.update({'stateCode': state, 'districtCode': district, 'subdistrictCode': subdistrict.subdistrictCode, 'villageCode': village.villageCode})
        #                         all_places.extend(village_places)
        #                     else:
        #                         return JsonResponse({'error': 'Invalid format for village places'}, status=500)
        #                 else:
        #                     return JsonResponse({'error': 'Failed to get village places'}, status=500)
                
        # JSONDataModel.objects.all().delete() # pylint: disable=maybe-no-member
        # for place in all_places:
        #     JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
        #     logging.info('JsonField Saved')
        # places = JSONDataModel.objects.all().values("jsonData") # pylint: disable=maybe-no-member   
        # print(places)
        # for place in places:
        #     data = place.get("jsonData")
        #     type_mapping = {
        #         'retail': ['shop', 'retail', 'mart', 'croma', 'oulet', 'store'],
        #         'food': ['food', 'restaurant', 'hotel', 'fastfood', ],
        #         'finance': ['Finance', 'solutions', 'consultant', 'planner'],
        #         'healthcare': ['healthcare', 'medical', 'labs', 'hospital','clinic'],
        #         'education': ['education', 'school', 'college', 'university', 'institute']
        #     }   
        #     if 'displayName' in data:
        #         display_name = str(data.get('displayName')).lower()
        #         place_catagory, created = CatagoryModel.objects.get_or_create(catagory="other") # pylint: disable=maybe-no-member

        #     # Iterate over the type mapping
        #     for catagory, keywords in type_mapping.items():
        #         for keyword in keywords:
        #             if keyword in display_name:
        #                 place_catagory, created = CatagoryModel.objects.get_or_create(catagory=catagory)  # pylint: disable=maybe-no-member
        #                 break
        #         if keyword in display_name:
        #             break
            # print(place_catagory.id)
            # print(data)         
            # data extraction 
            # DataModel.objects.get_or_create( name= data.get('displayName'),  # pylint: disable=maybe-no-member
            #                                 # catagory = place.jsonData.get('catagory'),
            #                                 catagory = place_catagory,                                    
            #                                 # primaryType = place.jsonData.get('primaryType'),
            #                                 formattedAddress = data.get('formattedAddress'),
            #                                 locationLongitude = data.get('location').get('lng'),
            #                                 locationLatitude = data.get('location').get('lat'),
            #                                 rating = data.get('rating'),
            #                                 # rating = None,
            #                                 googleMapsUri = data.get('googleMapsUri'),
            #                                 businessStatus = data.get('businessStatus'),
            #                                 userRatingCount = data.get('userRatingCount'),
            #                                 stateCode = data.get('stateCode'),
            #                                 districtCode = data.get('districtCode'),
            #                                 subdistrictCode = data.get('subdistrictCode'),
            #                                 villageCode = data.get('villageCode'),
            #                                 # userRatingCount = None
            #                                 # accessibilityOptions = []
            #                                 defaults={'id': data.get("uuid")}
            #                                 )
        # distinct_locations = DataModel.objects.only('stateCode','districtCode','subdistrictCode','villageCode','catagory').distinct() # pylint: disable=maybe-no-member
        # print("counting started")
        #     # After creating/updating DataModel entries, perform the counting operation
        # annotated_data = DataModel.objects.values('stateCode', 'districtCode', 'catagory').annotate(place_count=Count('id'))

        #         # Iterate over the annotated data and update the CountModel
        # for data in annotated_data:
        #         state_code = data.get('stateCode')
        #         district_code = data.get('districtCode')
        #         catagory_instance = CatagoryModel.objects.filter(pk=data['catagory']).first() 
        #         place_count = data['place_count']
        #         # print(catagory)
        #         CountModel.objects.update_or_create(
        #                 stateCode=state_code,
        #                 districtCode=district_code,
        #                 catagory=catagory_instance,
        #                 defaults={'count': place_count}
        #             )
        return HttpResponseRedirect(reverse('display'))

    context['form'] = form
    return render(request, 'frontend/fetch.html', context)

def fetch_api_data(state,district):
    '''fetching data from the api for the given district'''
    # print(state, district)
    if not state or not district:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    all_places = []
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
                    headers = {
                        "Content-Type": "application/json"
                    }
                    # making a request to all villages for places data
                    village_response = requests.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload), headers=headers)
                    if village_response.status_code == 200:
                        village_places = village_response.json().get("places", [])
                        # print(f"village_places: {village_places}")  # Debugging
                        if isinstance(village_places, list):
                            for place in village_places:
                                # print(f"place: {place}, type: {type(place)}")  # Debugging
                                if isinstance(place, dict):
                                    # adding location codes to the places returned by the api
                                    place.update({'stateCode': state, 'districtCode': district, 'subdistrictCode': subdistrict.subdistrictCode, 'villageCode': village.villageCode})
                            all_places.extend(village_places)
                        else:
                            return JsonResponse({'error': 'Invalid format for village places'}, status=500)
                    else:
                        return JsonResponse({'error': 'Failed to get village places'}, status=500)
    return all_places

def save_json(all_places):
    JSONDataModel.objects.all().delete() # pylint: disable=maybe-no-member
    for place in all_places:
        JSONDataModel.objects.get_or_create(jsonData = place) # pylint: disable=maybe-no-member
        logging.info('JsonField Saved')
    places = JSONDataModel.objects.all().values("jsonData") # pylint: disable=maybe-no-member 
    return places

def assign_category(places):
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

def count_places_by_catagory():
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


def display_view(request):
    '''To display distict districts and provide a option to view count'''
    distinct_locations = DataModel.objects.values('stateCode', # pylint: disable=maybe-no-member
                                                  'districtCode',
                                                  'catagory','created_at')  .distinct('stateCode',
                                                                        'districtCode')
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
    '''view to display the count for selected catagory'''
    state_code = request.GET.get('stateCode')
    district_code = request.GET.get('districtCode')
    district_name = request.GET.get('district_name')
    state_name = request.GET.get('state_name')
    print(state_name, district_name)
    all_catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if 'catagory' in request.session:
        catagoryChosen = request.session['catagory']
        catagory_id = CatagoryModel.objects.get(pk=catagoryChosen).id # pylint: disable=maybe-no-member
    else:
        catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if all_catagory_id == catagory_id:
        details = CountModel.objects.filter(stateCode=state_code, districtCode=district_code).values( # pylint: disable=maybe-no-member
            'stateCode', 'districtCode', 'catagory__catagory', 'count'
        )
        for detail in details: 
            detail.update({'district_name': district_name,'state_name': state_name })
    else:
        details = CountModel.objects.filter(stateCode=state_code, districtCode=district_code,catagory = catagory_id).values( # pylint: disable=maybe-no-member
            'stateCode', 'districtCode', 'catagory__catagory', 'count'
        )
        for detail in details: 
            detail.update({'district_name': district_name,'state_name': state_name })
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