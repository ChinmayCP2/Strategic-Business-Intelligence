'''models for the lgd app'''
from django.db import models

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

class StateModel(TimeStampedModel):
    '''
    Holds State related Information
    '''
    stateCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    stateNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    stateNameLocal = models.CharField(max_length=300,blank=True, null=True)

    def __str__(self):
    # the self.stateNameEnglish can be none so a empty string is attached
        return self.stateNameEnglish + ""
         


class DistrictModel(TimeStampedModel):
    '''
    Holds District related Information
    '''
    districtCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    districtNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    districtNameLocal = models.CharField(max_length=300,blank=True, null=True)
    stateCode = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    
    def __str__(self):
    # the self.districtNameEnglish can be none so a empty string is attached
        return self.districtNameEnglish + ""

class SubDistrictModel(TimeStampedModel):
    '''
    Holds District related Information
    '''
    subDistrictCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    subDistrictNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    subDistrictNameLocal = models.CharField(max_length=300,blank=True, null=True)
    districtCode = models.ForeignKey(DistrictModel, on_delete=models.CASCADE)
    def __str__(self):
    # the self.subDistrictNameEnglish can be none so a empty string is attached
        return self.subDistrictNameEnglish + ""
    
class VillageModel(TimeStampedModel):
    '''
    Holds District related Information
    '''
    villageCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    villageNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    villageNameLocal = models.CharField(max_length=300,blank=True, null=True)
    subSidtrictCode = models.ForeignKey(SubDistrictModel, on_delete=models.CASCADE)
    def __str__(self):
    # the self.villageNameEnglish can be none so a empty string is attached
        return self.villageNameEnglish + ""
