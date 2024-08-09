import json
import logging
import random
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
# from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Sum
# from django.db.models import Subquery
from django.db import connection
# from django.middleware.csrf import get_token
from django.core.paginator import Paginator
from dotenv import load_dotenv
from lgd.models import DistrictModel
from .forms import LocationForm, StateForm
# from utils.decorators import custom_permission_required
from .models import DataModel, CatagoryModel, CountModel
from .generate import generate_random_places
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
    logging.info("displayed the form")
    context = {}
    if 'catagory' in request.session:
            del request.session['catagory']
            logging.info("category saved in the session")
    if request.method == 'POST':   
        logging.info("Form submitted")
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        request.session['catagory'] = data.get('catagory')
        if DataModel.objects.filter(stateCode = state, districtCode = district).exists(): # pylint: disable=maybe-no-member
            logging.info("The district data found so redirected to display")
            return HttpResponseRedirect(reverse('display'))
        else:
            logging.info("The district data not found so redirected to fetch message")
            request.session['state'] = state
            request.session['district'] = district
            logging.info(f"redirect to fetch message {request.session['state']} and {request.session['district']} saved")
            return HttpResponseRedirect(reverse('fetch-message'))
    context['form'] = form
    context['page_name'] = "Home Page Form"
    return render(request, 'frontend/fetch.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_message(request):
    '''if district is not found message to ask user to fetch or continue'''
    logging.info("Feth message displayed")
    request.session['district']
    return render(request, 'frontend/fetch_message.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_function(request):
    '''fetch data from database'''
    logging.info("fetch function called")
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
            logging.info(f"state {request.session['state']} deleting after fetching is done ")
            del request.session['state']
            logging.info(f"state deleted after fetching is done ")
    if 'district' in request.session:
            logging.info(f"district {request.session['district']} deleting after fetching is done ")
            del request.session['district']
            logging.info(f"district deleted after fetching is done ")
    return HttpResponseRedirect(reverse('display'))


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
            logging.info(f"send_json called with {state_code},{district_code},{subdistrict_code} and {village_code}")
            if not state_code or not district_code:
                logging.error("state or district not found")
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            places = []
            if village_code:
                '''sending data for all the villages'''
                logging.info("random data generation started")
                places = generate_random_places(random.randint(0, 1))


            return JsonResponse({'places': places}, status=200)
        
        else:
            logging.error("invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    except json.JSONDecodeError:
        logging.error("invalid JSON")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logging.error(f"error {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_screen(request):
    '''fetch view'''
    logging.info("fetch screen called")

    form = LocationForm(request.POST or None)
    context = {}
    # deleting the previous catagory used by the user we we can set a new one when searching 
    if 'catagory' in request.session:
            logging.info("deleting category before fetching if any")
            del request.session['catagory']
    if request.method == 'POST':
        logging.info("Form submitted on fetch_screen")
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        # setting the category for displaying count
        request.session['catagory'] = data.get('catagory')
        request.session['state'] = state
        request.session['district'] = district
        logging.info("session data stored")
        fetch_function(request)
        # return render(request,'temp.html')
        return HttpResponseRedirect(reverse('display'))
    context['page_name'] = "Fetch    Page Form"
    context['form'] = form
    return render(request, 'frontend/fetch.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def display_view(request):
    '''To display distict districts and provide a option to view count''' 
    form = StateForm(request.POST or None)
    context = {}
    if request.method == 'POST' and request.POST.get('state'):
        data = request.POST
        state = data.get('state')
        rows = get_distinct_locations(state)
        logging.info("get district locations query ran based on state")
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish', 'districtCode','districtNameEnglish', 'created_at'], row)) for row in rows]
    else:


        logging.info("get district locations query ran for all states")
        rows = custom_sql_for_default_display()
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish', 'districtCode','districtNameEnglish', 'created_at'], row)) for row in rows]
    Paging = Paginator(updated_locations, 12)
    page_number = request.GET.get('page')
    locations = Paging.get_page(page_number)
    logging.info("Pagination is implemented")
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
    logging.info(f"get_details called with {state_name} , {district_name}")
    # print(state_name, district_name)
    all_catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if 'catagory' in request.session:
        catagoryChosen = request.session['catagory']
        logging.info(f"categoryChosen from session {catagoryChosen}")
        catagory_id = CatagoryModel.objects.get(pk=catagoryChosen).id # pylint: disable=maybe-no-member
    else:
        catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
        logging.info(f"category not chosen so displaying all")
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
        logging.info(f"category vise data displayed")
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
        logging.info(f"category all data displayed")
    print(details)
    data = list(details)
    return JsonResponse(data, safe=False)       


def load_districts(request):
    '''dropdown district'''
    state = request.GET.get('state')
    districts = DistrictModel.objects.filter(stateCode = state) # pylint: disable=maybe-no-member
    logging.info("loding district data for dropdown")
    # print(districts)
    context = {'districts' : districts}
    return render(request, 'dropdown_options/district_options.html', context)
