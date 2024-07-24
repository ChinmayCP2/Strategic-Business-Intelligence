from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from lgd.models import StateModel, DistrictModel, SubDistrictModel, VillageModel
def home():
    return HttpResponse("temp")