from django.db import models
# from django.db.models import UniqueConstraint

import uuid 
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

class DataModel(TimeStampedModel):
    '''data model'''
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default= -1)
    catagory = models.CharField(max_length=200, null=True, blank=True)
    googleMapsUri = models.CharField(max_length=200, null=True, blank=True, default= 'url not found')
    businessStatus = models.CharField(max_length=200, null=True, blank=True, default='closed')
    formattedAddress = models.TextField(null=True, blank=True)
    locationLongitude = models.DecimalField(max_digits=9, decimal_places=7, default=0)
    locationLatitude = models.DecimalField(max_digits=10, decimal_places=7,default=0)
    userRatingCount = models.IntegerField(null=True, blank=True, default= -1)
    # accessibilityOptions = models.JSONField()
