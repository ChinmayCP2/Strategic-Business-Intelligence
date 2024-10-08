import uuid 
from django.db import models
# from django.db.models import UniqueConstraint

# Create your models here.
class TimeStampedModel(models.Model):
    '''
    TimeStamp for when data is created and updated
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''TimeStampModel is Abstract used for inheritence'''
        abstract = True

class JSONDataModel(TimeStampedModel):
    '''json data model'''
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jsonData = models.JSONField(null=True, blank=True)

    # class Meta:
    #     '''unique constraint'''
    #     constraints = [
    #         UniqueConstraint(fields=['data'], name='unique data')
    #     ]

class CatagoryModel(TimeStampedModel):
    '''catagory model'''
    catagory = models.CharField(max_length=200, null=True, blank=True, default="other")
    subCatagory = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.catagory + ""

class PhaseModel(TimeStampedModel):
    '''summery model to indicate phase'''
    phase = models.CharField(max_length=200,null=True,blank=True, default="Pending")
    def __str__(self):
        return self.phase + ""

class SummeryModel(TimeStampedModel):
    '''summery model to indicate phase'''
    # phase = models.ForeignKey(PhaseModel, blank=True, on_delete=models.SET_NULL, null=True)
    STATUS_CHOICES = (
    ("Completed", 'Completed'),
    ("Not started", 'Not started'),
    ("In-Progress", 'In-Progress'),
    ("Failed", "Failed")
    )
    fetch_status = models.CharField(default="Not started", choices=STATUS_CHOICES, max_length = 200)
    extraction_status = models.CharField(default="Not started", choices=STATUS_CHOICES, max_length = 200)
    aggregation_status = models.CharField(default="Not started", choices=STATUS_CHOICES, max_length = 200)
    fetch_start_time =models.DateTimeField(null=True, blank=True)
    fetch_end_time = models.DateTimeField(null=True, blank=True)
    extraction_start_time = models.DateTimeField(null=True, blank=True)
    extraction_end_time = models.DateTimeField(null=True, blank=True)
    aggregation_start_time = models.DateTimeField(null=True, blank=True)
    aggregation_end_time = models.DateTimeField(null=True, blank=True)
    districtCode = models.IntegerField(null=True, blank=True)
    district_name = models.CharField(max_length=200, null=True, blank=True)
    state_name = models.CharField(max_length=200, null=True, blank=True)
    stateCode = models.IntegerField(null=True, blank=True)
    

class DataModel(TimeStampedModel):
    '''data model'''
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default= -1)
    catagory = models.ForeignKey(CatagoryModel, blank=True, on_delete=models.SET_NULL, null=True)

    # primaryType = models.CharField(max_length=200, null=True, blank=True)
    googleMapsUri = models.CharField(max_length=200, null=True, blank=True, default= 'url not found')
    businessStatus = models.CharField(max_length=200, null=True, blank=True, default='closed')
    formattedAddress = models.TextField(null=True, blank=True)
    locationLongitude = models.DecimalField(max_digits=10, decimal_places=7, default=0) 
    locationLatitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    userRatingCount = models.IntegerField(null=True, blank=True, default= -1)
    stateCode = models.IntegerField( null=True, blank=True, default=-1)
    districtCode = models.IntegerField(null=True, blank=True, default=-1)
    subdistrictCode = models.IntegerField( null=True, blank=True, default=-1)
    villageCode = models.IntegerField( null=True, blank=True, default=-1)
    # accessibilityOptions = models.JSONField()

class CountModel(TimeStampedModel):
    '''count aggregation table'''
    stateCode = models.IntegerField( null=True, blank=True)
    districtCode = models.IntegerField(null=True, blank=True, default=-1)
    subdistrictCode = models.IntegerField( null=True, blank=True, default=-1)
    villageCode = models.IntegerField( null=True, blank=True, default=-1)
    catagory = models.ForeignKey(CatagoryModel, blank=True, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['stateCode', 'districtCode', 'catagory']),
        ]
    