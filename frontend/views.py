from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from lgd.models import DistrictModel, SubDistrictModel, VillageModel, StateModel
from .forms import LocationForm, RegistrationForm
from strategicbi.models import DataModel, CountModel

# Create your views here.

@login_required(login_url='/login')
def home(request):
    '''index'''
    form = LocationForm(request.POST or None)
    context = {}
    if request.method == 'POST':   
        data = request.POST
        state = data.get('state')
        district = data.get('district')
        subdistrict = data.get('subdistrict')
        village = data.get('village')
        catagory = data.get('catagory')
        sorting = data.get('sorting')
        print(district)
        # print(state, village, subdistrict, district)
        fields = [field.name for field in DataModel._meta.get_fields()]  # pylint: disable=maybe-no-member
        dataFields = ["name","formattedAddress", "rating","userRatingCount", "googleMapsUri", "businessStatus"]
        if village:
            print('village working')
            try:
                state_instance = StateModel.objects.filter(pk=state).first() # pylint: disable=maybe-no-member
                district_instance = DistrictModel.objects.filter(pk=district,stateCode=state_instance).first() # pylint: disable=maybe-no-member
                subdistrict_instance = SubDistrictModel.objects.filter(pk=subdistrict,    # pylint: disable=maybe-no-member
                                                                        districtCode = district_instance,
                                                                        stateCode = state_instance).first() 
                village_instance = VillageModel.objects.filter(pk=village,    # pylint: disable=maybe-no-member
                                                                subdistrictCode = subdistrict_instance,
                                                                districtCode = district_instance,
                                                                stateCode = state_instance).values('villageCode').first() 
                if not village_instance:
                    context = {'message': 'District not found'}
                else:
                    state_code = state_instance.stateCode
                    district_code = district_instance.districtCode
                    subdistrict_code = subdistrict_instance.get('subdistrictCode')
                    village_code = village_instance.get('villageCode')
                    print(state_code, district_code,village_code)
                        
                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                        subdistrictCode = subdistrict_code,
                                                        villageCode = village_code,
                                                        catagory=catagory).order_by(sorting).values(*dataFields) 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                        subdistrictCode = subdistrict_code, 
                                                        villageCode = village_code,
                                                        catagory=catagory).values(*dataFields) 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code, # pylint: disable=maybe-no-member
                                                        districtCode = district_code,
                                                        villageCode = village_code,
                                                        subdistrictCode = subdistrict_code).values(*dataFields) 
                    # print(places)
                    if not places:
                        context = {'message': "No places found"}
                    else:
                        context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}
        elif subdistrict:
            print('subdist working')
            try:
                state_instance = StateModel.objects.filter(pk=state).first() # pylint: disable=maybe-no-member
                district_instance = DistrictModel.objects.filter(pk=district,stateCode=state_instance).first() # pylint: disable=maybe-no-member
                subdistrict_instance = SubDistrictModel.objects.filter(pk=subdistrict,    # pylint: disable=maybe-no-member
                                                                       districtCode = district_instance,
                                                                       stateCode = state_instance) \
                                                                       .values('subdistrictCode').first() 
                if not subdistrict_instance:
                    context = {'message': 'District not found'}
                else:
                    state_code = state_instance.stateCode
                    district_code = district_instance.districtCode
                    subdistrict_code = subdistrict_instance.get('subdistrictCode')
                    print(state_code, district_code, subdistrict_code)

                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                           subdistrictCode = subdistrict_code,
                                                           catagory=catagory).order_by(sorting).values(*dataFields) 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                          subdistrictCode = subdistrict_code, 
                                                           catagory=catagory).values(*dataFields) 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code, # pylint: disable=maybe-no-member
                                                           districtCode = district_code,
                                                           subdistrictCode = subdistrict_code).values(*dataFields) 
                    # print(places)
                    if not places:
                        context = {'message': "No places found"}
                    else:
                        context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}
        elif district:
            print('dist working')
            try:
                state_instance = StateModel.objects.filter(pk=state).first() # pylint: disable=maybe-no-member
                print(state_instance)
                district_instance = DistrictModel.objects.filter(pk=district,stateCode=state_instance).values('districtCode').first() # pylint: disable=maybe-no-member
                print(district_instance)
                if not district_instance:
                    context = {'message': 'District not found'}
                else:
                    state_code = state_instance.stateCode
                    print(state_code)
                    district_code = district_instance.get('districtCode')
                    print(district_code)
                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).order_by(sorting).values(*dataFields) 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).values(*dataFields) 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code, districtCode = district_code).values(*dataFields) # pylint: disable=maybe-no-member
                    # print(places)
                    if not places:
                        context = {'message': "No places found"}
                    else:
                        context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}
        else:
            print("state working")
            try:
                state_instance = StateModel.objects.filter(pk=state).values('stateCode').first() # pylint: disable=maybe-no-member
                print(state_instance.get('stateCode'))
                
                if not state_instance:
                    context = {'message': 'State not found'}
                else:
                    state_code = state_instance.get('stateCode')

                    if sorting and sorting in fields and catagory:
                        places = DataModel.objects.filter(stateCode=state_code, # pylint: disable=maybe-no-member
                                                           catagory=catagory).order_by(sorting).values(*dataFields) 
                    elif catagory:
                        places = DataModel.objects.filter(stateCode=state_code,  # pylint: disable=maybe-no-member
                                                           catagory=catagory).values(*dataFields) 
                    else:
                        places = DataModel.objects.filter(stateCode=state_code).values(*dataFields) # pylint: disable=maybe-no-member
                    # print(places)
                    if not places:
                        context = {'message': "No places found"}
                    else:
                        context = {'places': places}
            except Exception as e:
                context = {'message': 'An error occurred: {}'.format(str(e))}
    context['form'] = form
    return render(request, 'frontend/home.html', context)

# def view_all(request):
#     '''view to display all locations with places'''
#     counts = CountModel.objects.all() # pylint: disable=maybe-no-member
#     locations = []
#     for count in counts:
#         if count.villageCode:
#             state = StateModel.objects.filter(stateCode = count.stateCode).values("stateNameEnglish").first() # pylint: disable=maybe-no-member
#             district = DistrictModel.objects.filter(districtCode = count.districtCode).values("districtNameEnglish").first() # pylint: disable=maybe-no-member
#             subdistrict = SubDistrictModel.objects.filter(subdistrictCode = count.subdistrictCode).values("districtNameEnglish").first() # pylint: disable=maybe-no-member
#             village = VillageModel.objects.filter(villageCode = count.villageCode).values("villageNameEnglish").first() # pylint: disable=maybe-no-member
#             no = count.count
#             location = {"state": state.get("stateNameEnglish"),
#                         "district": district.get("districtNameEnglish"),
#                         "subdistrict": subdistrict.get("subdistrictNameEnglish"),
#                         "village": village.get("villageNameEnglish"),
#                         "count": no}
#             locations.append(location)
#         elif count.subdistrictCode:
#             state = StateModel.objects.filter(stateCode = count.stateCode).values("stateNameEnglish").first() # pylint: disable=maybe-no-member
#             district = DistrictModel.objects.filter(districtCode = count.districtCode).values("districtNameEnglish").first() # pylint: disable=maybe-no-member
#             subdistrict = SubDistrictModel.objects.filter(subdistrictCode = count.subdistrictCode).values("subdistrictNameEnglish").first() # pylint: disable=maybe-no-member
#             no = count.count
#             location = {"state": state.get("stateNameEnglish"),
#                         "district": district.get("districtNameEnglish"),
#                         "subdistrict": subdistrict.get("subdistrictNameEnglish"),
#                         "village": "",
#                         "count": no}
#             locations.append(location)
#         elif count.districtCode:
#             state = StateModel.objects.filter(stateCode = count.stateCode).values("stateNameEnglish").first() # pylint: disable=maybe-no-member
#             district = DistrictModel.objects.filter(districtCode = count.districtCode).values("districtNameEnglish").first() # pylint: disable=maybe-no-member
#             subdistrict = SubDistrictModel.objects.filter(subdistrictCode = count.subdistrictCode).values("subdistrictNameEnglish").first() # pylint: disable=maybe-no-member
#             no = count.count
#             location = {"state": state.get("stateNameEnglish"),
#                         "district": district.get("districtNameEnglish"),
#                         "subdistrict": "",
#                         "village": "",
#                         "count": no}
#             locations.append(location)
#         else:
#             state = StateModel.objects.filter(stateCode = count.stateCode).values("stateNameEnglish").first() # pylint: disable=maybe-no-member
#             no = count.count
#             location = {"state": state.get("stateNameEnglish"),
#                         "district": "",
#                         "subdistrict": "",
#                         "village": "",
#                         "count": no}
#             locations.append(location)
#     print(locations)
#     return render(request, 'view_all.html', {'locations': locations})



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

def load_subdistricts(request):
    '''dropdown of subdistrict'''
    district_code = request.GET.get('district')
    # print(district_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    subdistricts = SubDistrictModel.objects.filter(districtCode = district_code)# pylint: disable=maybe-no-member
    # print(subdistricts)
    context = {'subdistricts' : subdistricts}
    return render(request, 'dropdown_options/subdistrict_options.html', context)

def load_villages(request):
    '''dropdown of subdistrict'''
    subdistrict_code = request.GET.get('subdistrict')
    print(subdistrict_code)
    # state = StateModel.objects.get(id= state_id) # pylint: disable=maybe-no-member
    # print(state)
    villages = VillageModel.objects.filter(subdistrictCode = subdistrict_code)# pylint: disable=maybe-no-member
    # print(villages)
    context = {'villages' : villages}
    return render(request, 'dropdown_options/village_options.html', context)

