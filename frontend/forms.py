from django import forms
from lgd.models import StateModel, DistrictModel, SubDistrictModel, VillageModel

class LocationForm(forms.Form):
    # stateCode = forms.ModelChoiceField(queryset=StateModel.objects.all(),  # pylint: disable=maybe-no-member
    #                                 widget=forms.Select(attrs={"hx-get": "load-districts/","hx-target" : "#id_district", "hx-trigger": "change" }))
    stateCode = forms.ModelChoiceField(queryset=StateModel.objects.all(),  
                                   widget=forms.Select(attrs={"hx-get": "/load-districts/?stateCode={{ value }}", 
                                                             "hx-target" : "#id_district", 
                                                            }))
    district = forms.ModelChoiceField(queryset=DistrictModel.objects.none(),
                                      widget=forms.Select(attrs={"hx-get": "/load-subdistricts/?district={{ value }}", 
                                                             "hx-target" : "#id_subdistrict",
                                                            })) # pylint: disable=maybe-no-member
    subdistrict = forms.ModelChoiceField(queryset=SubDistrictModel.objects.none(),
                                         widget=forms.Select(attrs={"hx-get": "/load-villages/?subdistrict={{ value }}", 
                                                             "hx-target" : "#id_village", 
                                                            })) # pylint: disable=maybe-no-member
    village = forms.ModelChoiceField(queryset=VillageModel.objects.none()) # pylint: disable=maybe-no-member