from .models import *
import threading
from .views import fetch_function

class FetchPlacesThread(threading.Thread):
    def __init__(self,request):
        self.request = request  

    def run(self):
        try:
            fetch_function()
        except Exception as e:
            print(e)