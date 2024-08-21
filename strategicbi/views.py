'''views strageticbi'''
import csv
import json
import logging
import random
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.db.models import Sum
from django.db import connection
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from dotenv import load_dotenv
# from django.contrib.messages import get_messages
# from django.core.cache import cache
from lgd.models import DistrictModel, StateModel
from .forms import LocationForm, StateForm, CategoryForm
from .models import CatagoryModel, CountModel, SummeryModel
from .generate import generate_random_places
from .tasks import fetch_and_save_data

# Create your views here.
load_dotenv()
logger = logging.getLogger("strategicbi")

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='/login')
# def home(request):
#     '''Home view'''
#     form = LocationForm(request.POST or None)
#     logger.info("displayed the form")
#     context = {}
#     if 'catagory' in request.session:
#         # deleting previously saved category
#         del request.session['catagory']
#         logger.info("category saved in the session")
#     if request.method == 'POST':
#         logger.info("Form submitted")
#         data = request.POST
#         state = data.get('state')
#         district = data.get('district')
#         request.session['catagory'] = data.get('catagory')
#         if DataModel.objects.filter(stateCode = state, districtCode = district).exists(): # pylint: disable=maybe-no-member
#             # if district data is present display view is loaded
#             logger.info("The district data found so redirected to display")
#             # time.sleep(3)
#             return HttpResponseRedirect(reverse('fetch'))
#         else:
#             # sending user a message if he wishes to fetch the district data 
#             logger.info("The district data not found so redirected to fetch message")
#             request.session['state'] = state
#             request.session['district'] = district
#             logger.info("redirect to fetch message %s and %s saved",request.session['state'],
#                         request.session['district'])
#             return HttpResponseRedirect(reverse('fetch-message'))
#     # displaying last 10 districts loaded and thier status
#     summeries = SummeryModel.objects.filter(~Q(aggrigation_status = "Completed")).order_by('updated_at').values('updated_at', # pylint: disable=maybe-no-member
#                                                                            'state_name',
#                                                                            'district_name',
#                                                                            'fetch_status',
#                                                                            'extraction_status',
#                                                                            'aggrigation_status')[:10][::-1]
#     # print(summeries)
#     context['summeries'] = summeries
#     context['form'] = form
#     context['page_name'] = "Home Page Form"
#     return render(request, 'frontend/fetch.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_message(request):
    '''if district is not found message to ask user to fetch or continue'''
    logger.info("Feth message displayed")
    return render(request, 'frontend/fetch_message.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_function(request):
    '''fetch data from database'''
    logger.info("fetch function called")
    state = request.session['state'] 
    district = request.session['district'] 
    state_name = StateModel.objects.filter(pk=state).values('stateNameEnglish').first()  # pylint: disable=maybe-no-member
        # print(state)
    # print(state_name) 
    district_name = DistrictModel.objects.filter(pk=district).values('districtNameEnglish').first()  # pylint: disable=maybe-no-member
    # checking if the district chosen is already in a task or if its pending 
    district_status = SummeryModel.objects.filter(stateCode = state, # pylint: disable=maybe-no-member
                                                  districtCode = district)
    print(district_status.values('district_name'))
    if district_status.exists():
        # if yes the task is not started
        # SummeryModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
        #                              districtCode=district).update(fetch_status = "Failed",
        #                              extraction_status = "Failed",
        #                              aggrigation_status = "Failed")
        messages.warning(request, "The District is already processing")
    else:
        SummeryModel.objects.create(stateCode=state, # pylint: disable=maybe-no-member
                                        districtCode=district,
                                        district_name = district_name.get("districtNameEnglish"),
                                        state_name = state_name.get("stateNameEnglish"), 
                                        fetch_status = "In-Progress",
                                        extraction_status = "Not Started",
                                        aggrigation_status = "Not Started",
                                        fetch_start_time = datetime.datetime.now())
        fetch_and_save_data.delay(state, district)
        # deleting previously saved state and district for the next process
        if 'state' in request.session:
                logger.info("state %s deleting after fetching is done ", request.session['state'])
                del request.session['state']
                logger.info("state deleted after fetching is done ")
        if 'district' in request.session:
                logger.info("district %s deleting after fetching is done",request.session['district'])
                del request.session['district']
                logger.info("district deleted after fetching is done ")
        messages.success(request, "The Processing for the requested data has begun...")
        # if 'task_message' in request.session:
        #     messages.success(request, request.session.pop('task_message'))
    return HttpResponseRedirect(reverse('fetch'))


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
            logger.info("send_json called with %s, %s, %s and %s",state_code,district_code,
                        subdistrict_code,
                         village_code)
            if not state_code or not district_code:
                # if state or district is not found we return a error 
                logger.error("state or district not found")
                return JsonResponse({'error': 'Missing required parameters'}, status=400)

            places = []
            if village_code:
                logger.info("random data generation started")
                # generating random data
                places = generate_random_places(random.randint(1, 2))

            print(places)
            return JsonResponse({'places': places}, status=200)
        
        else:
            logger.error("invalid request method")
            return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    except json.JSONDecodeError:
        logger.error("invalid JSON")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error("error %s", str(e))
        return JsonResponse({'error': str(e)}, status=500)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def fetch_screen(request):
    '''fetch view'''
    logger.info("fetch screen called")
    form = LocationForm(request.POST or None)
    context = {}
    # deleting the previous catagory used by the user we we can set a new one when searching 
    if 'catagory' in request.session:
            # deleting previously saved category
            logger.info("deleting category before fetching if any")
            del request.session['catagory']
    if request.method == 'POST':
        logger.info("Form submitted on fetch_screen")
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        # setting the category for displaying count
        request.session['catagory'] = data.get('catagory')
        request.session['state'] = state
        request.session['district'] = district
        logger.info("session data stored")
        # redirecting to the fetch function view
        fetch_function(request)
        # return render(request,'temp.html')
        # time.sleep(3)
        return HttpResponseRedirect(reverse('fetch'))
    # displaying last 10 districts loaded and thier status
    summeries = SummeryModel.objects.filter(~Q(aggrigation_status = "Completed")).order_by('updated_at').values('updated_at', # pylint: disable=maybe-no-member
                                                                           'state_name',
                                                                           'district_name',
                                                                           'fetch_status',
                                                                           'extraction_status',
                                                                           'aggrigation_status')[:10][::-1]
    print(summeries)
    context['summeries'] = summeries
    context['page_name'] = "Fetch Page Form"
    context['form'] = form
    return render(request, 'frontend/fetch.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login')
def display_view(request):
    '''To display distict districts and provide a option to view count''' 
    form = StateForm(request.POST or None)
    catagory_form = CategoryForm(request.POST or None)
    context = {}
    if request.method == 'POST' and request.POST.get('state'):
        data = request.POST
        state = data.get('state')
        rows = get_distinct_locations(state)
        logger.info("get district locations query ran based on state")
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish', 
                                       'districtCode','districtNameEnglish',
                                         'created_at'], row)) for row in rows]
    else:
        logger.info("get district locations query ran for all states")
        rows = custom_sql_for_default_display()
        updated_locations = [dict(zip(['stateCode', 'stateNameEnglish',
                                        'districtCode','districtNameEnglish',
                                          'created_at'], row)) for row in rows]
    if request.method == 'POST' and request.POST.get('catagory'):
        data = request.POST
        catagory = data.get('catagory')
        request.session['catagory'] = catagory
        
    Paging = Paginator(updated_locations, 8)
    page_number = request.GET.get('page')
    locations = Paging.get_page(page_number)
    logger.info("Pagination is implemented")
    if not updated_locations:
        context = {
            'message' : "No result found"
        }
    else:
        context = {
            'distinct_locations': locations,
        }
    context['state_form'] = form
    context['catagory_form'] = catagory_form
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
    '''sql for get district location'''
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
    logger.info("get_details called with %s, %s ",state_name , district_name)
    # print(state_name, district_name)
    all_catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
    if 'catagory' in request.session:
        catagoryChosen = request.session['catagory']
        logger.info("categoryChosen from session %s", {catagoryChosen})
        catagory_id = CatagoryModel.objects.get(pk=catagoryChosen).id # pylint: disable=maybe-no-member
        catagory__catagory = CatagoryModel.objects.get(pk=catagoryChosen).catagory # pylint: disable=maybe-no-member
    else:
        catagory_id = CatagoryModel.objects.filter(catagory="all").first().id # pylint: disable=maybe-no-member
        logger.info("category not chosen so displaying all")
    if all_catagory_id == catagory_id:
        details = CountModel.objects.filter( # pylint: disable=maybe-no-member
            stateCode=state_code,
            districtCode=district_code
            ).values(
                'stateCode', 
                'districtCode', 
                'catagory__catagory'
            ).annotate(
                count=Sum('count')
            )   
        # for detail in details: 
        #     detail.update({'district_name': district_name,'state_name': state_name })
        
        logger.info("category vise data displayed")
    else:
        details = CountModel.objects.filter(   # pylint: disable=maybe-no-member
            stateCode=state_code, 
            districtCode=district_code,
            catagory__catagory = catagory__catagory,
            ).values(
                'stateCode', 
                'districtCode',
                'catagory__catagory',
                'catagory__subCatagory'
            ).annotate(
                count=Sum('count')
            ).exclude(catagory__subCatagory__isnull=True)
        # for detail in details:
        #     detail.update({'district_name': district_name,'state_name': state_name })
        print(details)
        logger.info("category all data displayed")
    # print(details)
    data = list(details)
    print(details)
    request.session['data'] = data
    # print(data)
    return JsonResponse(data, safe=False)  

@login_required(login_url='/login')
def get_processing_time_details(request):
    '''process details'''
    state_code = request.GET.get('stateCode')
    district_code = request.GET.get('districtCode')
    logger.info("get_details called with %s, %s ",state_code , district_code)
    district_summery = SummeryModel.objects.filter(stateCode = state_code, # pylint: disable=maybe-no-member
                                                    districtCode = district_code).first()
    fetch_time = district_summery.fetch_end_time - district_summery.fetch_start_time
    extratcion_time = district_summery.extraction_end_time - district_summery.extraction_start_time
    aggrigation_time = district_summery.aggrigation_end_time - district_summery.aggrigation_start_time
    context = {
        'aggrigation_time' : aggrigation_time.total_seconds(),
        'fetch_time' : fetch_time.total_seconds(),
        'extraction_time' : extratcion_time.total_seconds()
    }
    # print(extratcion_time.total_seconds())
    return JsonResponse(context, safe=False)


def download_csv(request):
    '''download csv function'''
    data = request.session['data']
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = "attachment;filename=export.csv"
    # the csv writer
    writer = csv.writer(response)
    field_names = ['category','count']
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in data:
        # print(obj)
        writer.writerow([obj.get('catagory__catagory'), obj.get('count')])
    return response

def load_districts(request):
    '''dropdown district'''
    state = request.GET.get('state')
    districts = DistrictModel.objects.filter(stateCode = state) # pylint: disable=maybe-no-member
    logger.info("loding district data for dropdown")
    context = {'districts' : districts}
    return render(request, 'dropdown_options/district_options.html', context)