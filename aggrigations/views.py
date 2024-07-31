import json
from django.http import JsonResponse
from django.db import connection
from django.db.models import Sum,Avg
from strategicbi.models import DataModel

# Create your views here.

def load_place_state(request):
    '''to get places in specific state'''
    try:
        data = request.GET
        state = data.get('stateCode')
        sorting = data.get('sorting')
        catagory = data.get('catagory')
        print(sorting)
        
        if not state:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        fields = [field.name for field in DataModel._meta.get_fields()]  # pylint: disable=maybe-no-member
        if sorting and sorting in fields and catagory:
            places = DataModel.objects.filter(stateCode=state,  # pylint: disable=maybe-no-member
                                              catagory=catagory).order_by(sorting).values("name") 
            # print("sorting ran")
        elif catagory:
            places = DataModel.objects.filter(stateCode=state, # pylint: disable=maybe-no-member
                                              catagory=catagory).values("name") 
        else:
            places = DataModel.objects.filter(stateCode=state).values("name") # pylint: disable=maybe-no-member
        return JsonResponse(list(places), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def load_place_district(request):
    '''to get places in specific state'''
    try:
        data = request.GET
        state = data.get('stateCode')
        district = data.get('districtCode')
        

        if not state or not district:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
            # print(state)
            # print(village)
        places = DataModel.objects.filter(stateCode=state,  # pylint: disable=maybe-no-member
                                          districtCode = district).values('name', 'districtCode')
        return JsonResponse(list(places), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def load_place_subdistrict(request):
    '''to get places in specific state'''
    try:
        data = request.GET
        state = data.get('stateCode')
        district = data.get('districtCode')
        subdistrict = data.get('subdistrictCode')

        if not state or not district or not subdistrict:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
            # print(state)
            # print(village)
        places = DataModel.objects.filter(stateCode=state, districtCode = district, # pylint: disable=maybe-no-member
                                       subdistrictCode = subdistrict).values('name', 'districtCode')
        return JsonResponse(list(places), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def load_place_village(request):
    '''to get places in specific state'''
    try:
        data = request.GET
        state = data.get('stateCode')
        district = data.get('districtCode')
        subdistrict = data.get('subdistrictCode')
        village = data.get('villageCode')

        if not state or not district or not subdistrict or not village:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
            # print(state)
            # print(village)
        places = DataModel.objects.filter(stateCode=state, districtCode = district, # pylint: disable=maybe-no-member
                                       subdistrictCode = subdistrict,
                                       villageCode = village).values('name', 'districtCode')
        return JsonResponse(list(places), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
     


def load_places(request):
    '''to get all places'''
    try:
        if request.method == "GET":
            places = list(DataModel.objects.all().values('name', 'stateCode'))  # pylint: disable=maybe-no-member
            return JsonResponse(places, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST method not allowed'}, status=405)

def get_total_user_ratings(request):
    try:
        if request.method == "GET":
            data = request.GET
            state = data.get('stateCode')
            catagory = data.get('catagory')
            if catagory:
                total_ratings = DataModel.objects.filter(stateCode=state, catagory=catagory).aggregate(Avg('rating')) # pylint: disable=maybe-no-member
                print(connection.queries)
            else:
                total_ratings = DataModel.objects.filter(stateCode = state).aggregate(Avg('rating')) # pylint: disable=maybe-no-member
            return JsonResponse({'total_ratings': total_ratings}, safe=False)

            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)