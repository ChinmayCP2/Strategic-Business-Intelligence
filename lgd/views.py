'''http response'''
import os
import logging
from dotenv import load_dotenv
import requests
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import StateModel, DistrictModel, SubDistrictModel, VillageModel

load_dotenv()
logger = logging.getLogger('lgd')

@permission_required('auth_app.lgd_access')  
def load_state(request):
    '''function to load the states'''
    print('working')
    try:
        request_to_lgd = requests.post(os.getenv('STATE_ENDPOINT'), 
                          data=request.POST, timeout=100)
    except requests.exceptions.Timeout:
        # print("Timed out")
        logger.error("Time out",exc_info=True)
    if request_to_lgd.status_code == 200:
        data = request_to_lgd.json()
        for state in data:
            state.pop("census2011Code")
            state.pop("census2001Code")
        state_instances = [StateModel(**state) for state in data]
        # print(data)
        StateModel.objects.bulk_create(state_instances, ignore_conflicts=True) # pylint: disable=maybe-no-member        
        logger.info('State Data saved to the database')
        return HttpResponse("state data saved")
           
    logger.error('state data not saved to the database with status code %s',
                  request_to_lgd.status_code)
    return HttpResponse('Could not save data')

@permission_required('auth_app.lgd_access')  
def load_district(request):
    '''loads district data'''
    states = StateModel.objects.all().distinct() # pylint: disable=maybe-no-member
    # print(states)
    for state in states:
        try:
            request_to_lgd = requests.post(os.getenv('DISTRICT_ENDPOINT') + f"{state.stateCode}",   
                            data=request.POST, timeout=100000)
        except requests.exceptions.Timeout:
                # print("Timed out")
                logger.error("Time out",exc_info=True)
        if request_to_lgd.status_code == 200:
            data = request_to_lgd.json()
            for district in data:
                district.pop("census2011Code")
                district.pop("census2001Code")
                district.pop("sscode")
            district_instances = [DistrictModel( stateCode=state, **district) for district in data]
            # print(data)
            DistrictModel.objects.bulk_create(district_instances, ignore_conflicts=True) # pylint: disable=maybe-no-member
            # print('district data saved')
        else:
            print('district data not saved')
            logger.error('district Data not saved')
            return HttpResponse("district data not saved")
    logger.info('District Data saved')
    return HttpResponse("district data saved")

@permission_required('auth_app.lgd_access')   
def load_sub_district(request):
    '''loads subdistrict data'''
    print('working')
    # SubDistrictModel.objects.all().delete() # pylint: disable=maybe-no-member
    districts = DistrictModel.objects.all().distinct() # pylint: disable=maybe-no-member
    # print(districts)
    for district in districts:
        try:
            request_to_lgd = requests.post( os.getenv('SUBDISTRICT_ENDPOINT') + f"{district.districtCode}", 
                            data=request.POST, timeout=None)
        except requests.exceptions.RequestException as e:
            # print("Timed out")
            logger.error("Exception in sending the subdistrict request - %s",e)
        except Exception as e:
            logger.error("Exception in sending the subdistrict request - %s",e)
        if request_to_lgd.status_code == 200:
            data = request_to_lgd.json()
            # print(data)
            for subdistrict in data:
                subdistrict.pop("census2011Code")
                subdistrict.pop("census2001Code")
                subdistrict.pop("sscode")
            subdistrict_instances = [SubDistrictModel(districtCode = district, stateCode = district.stateCode,
                                                       **subdistrict) for subdistrict in data]
            # print(data)
            SubDistrictModel.objects.bulk_create(subdistrict_instances, ignore_conflicts=True) # pylint: disable=maybe-no-member
                # print('subdistrict data saved')
        elif request_to_lgd.status_code == '503':
            logger.error('Service Unavailable with status code %s', request_to_lgd.status_code)
        else:
            # print('subdistrict data not saved')
            logger.info('subdistrict Data saved with status code %s', request_to_lgd.status_code)
            return HttpResponse("subdistrict data not saved")
    logger.info('subdistrict Data saved')
    return HttpResponse("subdistrict data saved")

@permission_required('auth_app.lgd_access')  
def load_village(request):
    '''loads village data'''
    print('working')
    # VillageModel.objects.all().delete() # pylint: disable=maybe-no-member
    subdistricts = SubDistrictModel.objects.all().distinct() # pylint: disable=maybe-no-member
    # print(subDistricts)
    for subdistrict in subdistricts:
        try:
            request_to_lgd = requests.post(os.getenv('VILLAGE_ENDPOINT') + f"{subdistrict.subdistrictCode}",
                                            data=request.POST, timeout=None) 
        except requests.exceptions.RequestException as e:
            # print("Timed out")
            logger.error("Exception in sending the subdistrict request - %s",e)
        except Exception as e:
            logger.error("Exception in sending the subdistrict request - %s",e)
        if request_to_lgd.status_code == 200:
            data = request_to_lgd.json()
            # print(data)
            for village in data:
                # print(village)
                village.pop("census2011Code")
                village.pop("census2001Code")
                village.pop("sscode")
            village_instances = [VillageModel(districtCode = subdistrict.districtCode,
                                               stateCode = subdistrict.districtCode.stateCode,
                                               subdistrictCode = subdistrict,
                                                 **village) for village in data]
            VillageModel.objects.bulk_create(village_instances, ignore_conflicts=True)
                
            # print('village data saved')
        else: 
            logger.error("Status code returned is not 200 error in the request")
            # print('district data not saved')
            return HttpResponse("subdistrict data not saved, error occured")
    logger.info('village data saved')       
    return HttpResponse("village data saved")

# @permission_required('frontend.lgd_access')
# def reset_db(request,region):
#     '''resets the database'''
#     if region == 'dist':
#         DistrictModel.objects.all().delete() # pylint: disable=maybe-no-member
#         logger.info("%s reset done", region)
#     elif region == 'state':
#         StateModel.objects.all().delete() # pylint: disable=maybe-no-member
#         logger.info("%s reset done", region)
#     elif region == 'subdist':
#         SubDistrictModel.objects.all().delete() # pylint: disable=maybe-no-member
#         logger.info("%s reset done", region)
#     elif region == 'village':
#         VillageModel.objects.all().delete() # pylint: disable=maybe-no-member
#         logger.info("%s reset done", region)
#     else:
#         logger.error("user entered invalid region")
#         return HttpResponse("region not specified")
#     return HttpResponse("database reset done")
    # print('database reset')

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