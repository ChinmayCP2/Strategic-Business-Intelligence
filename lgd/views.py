from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned
import requests
from .models import StateModel, DistrictModel, SubDistrictModel, VillageModel

def load_state(request):
    '''function to load the states'''
    StateModel.objects.all().delete() # pylint: disable=maybe-no-member
    # delete privious data
    try:
        r = requests.post('https://lgdirectory.gov.in/webservices/lgdws/stateList', 
                          data=request.POST, timeout=10)
    except requests.exceptions.Timeout:
        print("Timed out")
    if r.status_code == 200:
        data = r.json()
        # print(data)      
        for state in data:
            states = {
                "stateCode": state["stateCode"],
                "stateNameEnglish": state["stateNameEnglish"],
                "stateNameLocal": state["stateNameLocal"],
                }
            context = StateModel.objects.create(**states) # pylint: disable=maybe-no-member           
        # r.text, r.content, r.url, r.json
        # loading district data
        return HttpResponse("state data saved")        
    return HttpResponse('Could not save data')

def load_district(request):
    '''loads district data'''
    DistrictModel.objects.all().delete() # pylint: disable=maybe-no-member
    states = StateModel.objects.values("stateCode").distinct() # pylint: disable=maybe-no-member
    print(states)
    for state in states:
        try:
            r = requests.post(f"https://lgdirectory.gov.in/webservices/lgdws/districtList?stateCode={state['stateCode']}", 
                            data=request.POST, timeout=100000)
        except requests.exceptions.Timeout: 
                print("Timed out")
        if r.status_code == 200:
            data = r.json()
            state_instance = StateModel.objects.filter(stateCode=state['stateCode']).first() # pylint: disable=maybe-no-member   
            print(state_instance)
            for district in data:
                districts = {
                    "districtCode": district["districtCode"],
                    "districtNameEnglish": district["districtNameEnglish"],
                    "districtNameLocal": district["districtNameLocal"],
                    "stateCode" : state_instance
                    }
                context = DistrictModel.objects.create(**districts) # pylint: disable=maybe-no-member
                    # print('district data saved')
        else: 
            print('district data not saved')
            return HttpResponse("district data not saved")
    return HttpResponse("district data saved")
            
def load_sub_district(request):
    '''loads subdistrict data'''
    SubDistrictModel.objects.all().delete() # pylint: disable=maybe-no-member
    districts = DistrictModel.objects.values("districtCode").distinct() # pylint: disable=maybe-no-member
    # print(districts)
    for district in districts:
        try:
            r = requests.post(f"https://lgdirectory.gov.in/webservices/lgdws/subdistrictList?districtCode={district['districtCode']}", 
                            data=request.POST)
        except: 
                print("Timed out")
        if r.status_code == 200:
            data = r.json()
            district_instance = DistrictModel.objects.filter(districtCode=district['districtCode']).first() # pylint: disable=maybe-no-member   
            # print(district_instance)
            for subDistrict in data:
                # print(subDistrict)
                subDistricts = {
                    "subDistrictCode": subDistrict["subdistrictCode"],
                    "subDistrictNameEnglish": subDistrict["subdistrictNameEnglish"],
                    "subDistrictNameLocal": subDistrict["subdistrictNameLocal"],
                    "districtCode" : district_instance
                    }
                context = SubDistrictModel.objects.create(**subDistricts) # pylint: disable=maybe-no-member
                print('district data saved')
        else: 
            print('district data not saved')
            return HttpResponse("subdistrict data not saved")
    return HttpResponse("subdistrict data saved")

def load_village(request):
    '''loads village data'''
    VillageModel.objects.all().delete() # pylint: disable=maybe-no-member
    subDistricts = SubDistrictModel.objects.values("subDistrictCode").distinct() # pylint: disable=maybe-no-member
    # print(subDistricts)
    for subDistrict in subDistricts:
        try:
            r = requests.post(f"https://lgdirectory.gov.in/webservices/lgdws/villageList?subDistrictCode={subDistrict['subDistrictCode']}", 
                            data=request.POST)
        except: 
            print("Timed out")
        if r.status_code == 200:
            data = r.json()
            subDistrict_instance = SubDistrictModel.objects.filter(subDistrictCode=subDistrict['subDistrictCode']).first() # pylint: disable=maybe-no-member   
            print(subDistrict_instance)
            for village in data:
                print(village)
                villages = {
                    "villageCode": village["villageCode"],
                    "villageNameEnglish": village["villageNameEnglish"],
                    "villageNameLocal": village["villageNameLocal"],
                    "subSidtrictCode" : subDistrict_instance
                    }
                context = VillageModel.objects.create(**villages) # pylint: disable=maybe-no-member
                print('village data saved')
        else: 
            print('district data not saved')
            return HttpResponse("subdistrict data not saved")
    return HttpResponse("subdistrict data saved")

# class Load_region(View):
#     '''load Region data'''
#     def get(self, request, *args, **kwargs):
#         '''inserts data'''
#         StateModel.objects.all().delete() # pylint: disable=maybe-no-member
#         # delete privious data
#         parameter = dict(kwargs)
#         try:
#             url = "https://lgdirectory.gov.in/webservices/lgdws/stateList"
#             # url = str(kwargs.get("url"))
#             r = requests.post(url,
#                             data=request.POST, timeout=10)
#         except requests.exceptions.Timeout:
#             print("Timed out")
#         if r.status_code == 200:
#             data = r.json()
#             data.append(parameter)
#             data = {key: data[key] for key in args if key in data}

#             for state in data:
#                 try:
#                     context = StateModel.objects.create(**state) # pylint: disable=maybe-no-member
#                 except IntegrityError: 
#                     print("Duplicate record detected")
#         # r.text, r.content, r.url, r.json
#         return HttpResponse(r.text)

# class Load(Load_region):
#     '''load data'''
#     def get(self, request, *args, **kwargs):
#         url = "https://lgdirectory.gov.in/webservices/lgdws/stateList"
#         fields = ["stateCode", "stateNameEnglish", "stateNameLocal"]
#         # kwargs.update({"url" : url})
#         return super().get(request, *fields, url=url, **kwargs)