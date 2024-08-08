# import os
import json
import logging
import random
# import requests
# import asyncio
# from aiohttp import ClientSession
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Sum
# from django.db.models import Subquery
from django.db import connection
# from django.middleware.csrf import get_token
from django.core.paginator import Paginator
from dotenv import load_dotenv
from lgd.models import SubDistrictModel, StateModel, DistrictModel, VillageModel
from .forms import LocationForm, RegistrationForm, StateForm
# from utils.decorators import custom_permission_required
from .models import JSONDataModel, DataModel, CatagoryModel, CountModel
from .generate import generate_random_places
# from asgiref.sync import async_to_sync
from .tasks import fetch_and_save_data
# Create your views here.
load_dotenv()
logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
        if DataModel.objects.filter(stateCode = state, districtCode = district).exists(): # pylint: disable=maybe-no-member
            return HttpResponseRedirect(reverse('display'))
        else:
            request.session['state'] = state
            request.session['district'] = district
            return HttpResponseRedirect(reverse('fetch-message'))
    context['form'] = form
    context['page_name'] = "Home Page Form"
    return render(request, 'frontend/fetch.html', context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_message(request):
    '''if district is not found message to ask user to fetch or continue'''
    return render(request, 'frontend/fetch_message.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_function(request):
    '''fetch data from database'''
    state = request.session['state'] 
    district = request.session['district'] 
    # all_places = asyncio.run(fetch_api_data(state,district))
    # all_places = async_to_sync(fetch_api_data(state,district))(state,district)
    # all_places = fetch_api_data(state,district)
    # places = save_json(all_places)
    # assign_category(places)
    # count_places_by_catagory()
    fetch_and_save_data.delay(state, district)
    if 'state' in request.session:
            del request.session['state']
    if 'district' in request.session:
            del request.session['district']
    return HttpResponseRedirect(reverse('display'))

# async def fetch_api_data(state, district):
#     '''fetching data from the api for the given district'''
#     if not state or not district:
#         return JsonResponse({'error': 'Missing required parameters'}, status=400)

#     all_places = []
#     tasks = []
#     subdistricts = SubDistrictModel.objects.filter(districtCode=district)

#     async with ClientSession() as session:
#         for subdistrict in subdistricts:
#             villages = VillageModel.objects.filter(subdistrictCode=subdistrict)
#             for village in villages:
#                 village_payload = {
#                     "stateCode": state,
#                     "districtCode": district,
#                     "subdistrictCode": subdistrict.subdistrictCode,
#                     "villageCode": village.villageCode
#                 }
#                 tasks.append(fetch_village_places(session, village_payload))

#         results = await asyncio.gather(*tasks)
#         for result in results:
#             if result:
#                 all_places.extend(result)
            
#     print(all_places)
#     return all_places

# async def fetch_village_places(session, village_payload):
#     headers = {
#         "Content-Type": "application/json"
#     }
#     async with session.post(os.getenv('CATEGORICAL_DATA'), data=json.dumps(village_payload), headers=headers) as response:
#         if response.status == 200:
#             village_places = await response.json()
#             if isinstance(village_places, list):
#                 for place in village_places:
#                     if isinstance(place, dict):
#                         place.update({'stateCode': village_payload.get('stateCode'),
#                                        'districtCode': village_payload.get('districtCode'),
#                                          'subdistrictCode': village_payload.get('subdistrictCode'),
#                                            'villageCode': village_payload.get('villageCode')})
#                 return village_places
#             else:
#                 return JsonResponse({'error': 'Invalid format for village places'}, status=500)
#         else:
#             return JsonResponse({'error': 'Failed to get village places'}, status=500)


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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_screen(request):
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
        request.session['state'] = state
        request.session['district'] = district
        fetch_function(request)
        # return render(request,'temp.html')
        return HttpResponseRedirect(reverse('display'))
    context['page_name'] = "Fetch    Page Form"
    context['form'] = form
    return render(request, 'frontend/fetch.html', context)



@login_required(login_url='/login')
def display_view(request):
    '''To display distict districts and provide a option to view count''' 
    # distinct_locations = DataModel.objects.values('stateCode', # pylint: disable=maybe-no-member
    #                                               'districtCode',
    #                                               'catagory','created_at')  .distinct('stateCode',
    #                                                                     'districtCode')
    
    form = StateForm(request.POST or None)
    context = {}
    if request.method == 'POST' and request.POST.get('state'):
        data = request.POST
        state = data.get('state')
        # state_instance = StateModel.objects.get(id=state)  # Replace with the actual state object
        rows = get_distinct_locations(state)
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish', 'districtCode','districtNameEnglish', 'created_at'], row)) for row in rows]
        # subquery = DataModel.objects.filter(stateCode = state) \
        #                         .only('stateCode','districtCode','created_at') \
        #                         .distinct('stateCode',
        #                                 'districtCode')
        

        # distinct_locations = DataModel.objects.only('stateCode','districtCode','created_at') \
        #                             .filter(id__in=Subquery(subquery.values('id'))) \
        #                                 .values('stateCode', 
        #                                         'districtCode', 
        #                                         'catagory', 
        #                                         'created_at') \
        #                                 .order_by('-created_at')
        # updated_locations = []
        # for location in distinct_locations:
        #     state_code = location.get("stateCode")
        #     district_code = location.get("districtCode")
        #     state_name = StateModel.objects.get(pk=state_code).stateNameEnglish # pylint: disable=maybe-no-member
        #     district_name = DistrictModel.objects.get(pk=district_code).districtNameEnglish # pylint: disable=maybe-no-member
        #     # Update the location dictionary with state and district names
        #     location.update({'state_name': state_name, 'district_name': district_name}) 
        #     # Add the updated location to the list
        #     updated_locations.append(location)
    else:
        # subquery = DataModel.objects.only('stateCode','districtCode','created_at') \
        #                             .distinct('stateCode', 
        #                                     'districtCode')

        # distinct_locations = DataModel.objects.only('stateCode','districtCode','created_at') \
        #                             .filter(id__in=Subquery(subquery.values('id'))) \
        #                             .values('stateCode', 
        #                                     'districtCode', 
        #                                     'catagory', 
        #                                     'created_at') \
        #                             .order_by('-created_at')
        rows = custom_sql_for_default_display()
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish', 'districtCode','districtNameEnglish', 'created_at'], row)) for row in rows]
        # print(updated_locations)
        # updated_locations = []
        # for location in distinct_locations:
        #     state_code = location.get("stateCode")
        #     district_code = location.get("districtCode")
        #     state_name = StateModel.objects.get(pk=state_code).stateNameEnglish # pylint: disable=maybe-no-member
        #     district_name = DistrictModel.objects.get(pk=district_code).districtNameEnglish # pylint: disable=maybe-no-member
        #     # Update the location dictionary with state and district names
        #     location.update({'state_name': state_name, 'district_name': district_name}) 
        #     # Add the updated location to the list
        #     updated_locations.append(location)
        # print(distinct_locations)
    Paging = Paginator(updated_locations, 12)
    page_number = request.GET.get('page')
    locations = Paging.get_page(page_number)
    if not updated_locations:
        context = {
            'message' : "No result found"
        }
    else:
        context = {
            'distinct_locations': locations,
        }
    context['form'] = form
    return render(request, 'frontend/display.html', context)

# def my_custom_sql(self):
#     cursor = connection.cursor()    
#     cursor.execute("""select "lgd_statemodel"."id" as "stateCode", 
#                    "lgd_districtmodel"."id" as "districtCode",
#                    "lgd_statemodel"."stateNameEnglish" as "stateNameEnglish",
#                    "lgd_districtmodel"."districtNameEnglish" as "districtNameEnglish",
#                     from "strategicbi_datamodel" dm
#                     INNER JOIN "lgd_districtmodel" d ON dm."districtCode" = d."id"
#                     INNER JOIN "lgd_statemodel" s ON dm."stateCode" = s."id";""")
#     row = cursor.fetchone()
#     return row

def custom_sql_for_default_display():
    '''Query to get State district names with a inner join and thier codes'''
    cursor = connection.cursor()
    cursor.execute("""
        WITH distinct_locations AS (
        SELECT 
            "stateCode",
            "districtCode",
            MAX(created_at) AS created_at
        FROM 
            public.strategicbi_datamodel
        GROUP BY 
            "stateCode", 
            "districtCode"
        )
        SELECT 
        dl."stateCode" AS stateCode,
        s."stateNameEnglish" AS stateNameEnglish,
        dl."districtCode" AS districtCode,
        d."districtNameEnglish" AS districtNameEnglish,
        dl.created_at
        FROM 
        distinct_locations dl
        INNER JOIN public.lgd_statemodel s ON dl."stateCode" = s.id
        INNER JOIN public.lgd_districtmodel d ON dl."districtCode" = d.id
        ORDER BY 
        dl.created_at DESC;
    """)
    rows = cursor.fetchall()
    return rows

def get_distinct_locations(state):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH distinct_locations AS (
                SELECT 
                    "stateCode",
                    "districtCode",
                    MAX(created_at) AS created_at
                FROM 
                    public.strategicbi_datamodel
                GROUP BY 
                    "stateCode", 
                    "districtCode"
            )
            SELECT 
                dl."stateCode" AS stateCode,
                s."stateNameEnglish" AS stateNameEnglish,
                dl."districtCode" AS districtCode,
                d."districtNameEnglish" AS districtNameEnglish,
                dl.created_at
            FROM 
                distinct_locations dl
            INNER JOIN public.lgd_statemodel s ON dl."stateCode" = s.id
            INNER JOIN public.lgd_districtmodel d ON dl."districtCode" = d.id
            WHERE 
                s.id = %s
            ORDER BY 
                dl.created_at DESC
        """, [state])
        rows = cursor.fetchall()
    return rows

@login_required(login_url='/login')
def get_details(request):
    '''view to display the count for selected catagory'''
    state_code = request.GET.get('stateCode')
    district_code = request.GET.get('districtCode')
    district_name = request.GET.get('districtNameEnglish')
    state_name = request.GET.get('stateNameEnglish')
    # print(state_name, district_name)
    all_catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if 'catagory' in request.session:
        catagoryChosen = request.session['catagory']
        catagory_id = CatagoryModel.objects.get(pk=catagoryChosen).id # pylint: disable=maybe-no-member
    else:
        catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if all_catagory_id == catagory_id:
        details = CountModel.objects.filter(
            stateCode=state_code, 
            districtCode=district_code
            ).values(
                'stateCode', 
                'districtCode', 
                'catagory__catagory'
            ).annotate(
                count=Sum('count')
            )   
        for detail in details: 
            detail.update({'district_name': district_name,'state_name': state_name })
    else:
        # details = CountModel.objects.filter(stateCode=state_code, districtCode=district_code).values( # pylint: disable=maybe-no-member
        #     'stateCode', 'districtCode', 'catagory__catagory', 'count'
        # )
        details = CountModel.objects.filter(   # pylint: disable=maybe-no-member
            stateCode=state_code, 
            districtCode=district_code,
            catagory = catagory_id
            ).values(
                'stateCode', 
                'districtCode', 
                'catagory__catagory'
            ).annotate(
                count=Sum('count')
            )
        for detail in details: 
            detail.update({'district_name': district_name,'state_name': state_name })
    print(details)
    data = list(details)
    return JsonResponse(data, safe=False)       

    
def sign_up(request):
    '''Sign Up with a custom form'''
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