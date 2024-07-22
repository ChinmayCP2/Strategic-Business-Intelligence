from django.http import HttpResponse
import requests
from .models import StateModel
from django.db.utils import IntegrityError

def reload(request):
    StateModel.objects.all().delete()
    # delete privious data
    r = requests.post('https://lgdirectory.gov.in/webservices/lgdws/stateList', data=request.POST)
    if r.status_code == 200:
        data = r.json()
        # print(data)
        
        for state in data:
            states = {
                "stateCode": state["stateCode"],
                "stateNameEnglish": state["stateNameEnglish"],
                "stateNameLocal": state["stateNameLocal"]
                }
            context = StateModel.objects.create(**states)
        
        # r.text, r.content, r.url, r.json
        return HttpResponse(r.text)

    return HttpResponse('Could not save data')