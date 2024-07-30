from django import forms
from lgd.models import StateModel, DistrictModel, SubDistrictModel, VillageModel

class LocationForm(forms.Form):
    '''select location form'''
    # stateCode = forms.ModelChoiceField(queryset=StateModel.objects.all(),  # pylint: disable=maybe-no-member
    #                                 widget=forms.Select(attrs={"hx-get": "load-districts/","hx-target" : "#id_district", "hx-trigger": "change" }))
    stateCode = forms.ModelChoiceField(queryset=StateModel.objects.all(), required=True,
                                   widget=forms.Select(attrs={"hx-get": "/load-districts/?stateCode={{ value }}", 
                                                             "hx-target" : "#id_district", 
                                                            }))
    district = forms.ModelChoiceField(queryset=DistrictModel.objects.none(),required=False,
                                      widget=forms.Select(attrs={"hx-get": "/load-subdistricts/?district={{ value }}", 
                                                             "hx-target" : "#id_subdistrict",
                                                            })) # pylint: disable=maybe-no-member
    subdistrict = forms.ModelChoiceField(queryset=SubDistrictModel.objects.none(),required=False,
                                         widget=forms.Select(attrs={"hx-get": "/load-villages/?subdistrict={{ value }}", 
                                                             "hx-target" : "#id_village", 
                                                            })) # pylint: disable=maybe-no-member
    village = forms.ModelChoiceField(queryset=VillageModel.objects.none(),required=False) # pylint: disable=maybe-no-member