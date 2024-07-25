'''models for the lgd app'''
from django.db import models
from django.db.models import UniqueConstraint

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
    class Meta:
        constraints = [
            UniqueConstraint(fields=['stateCode'], name='unique state')
        ]



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
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['districtCode'], name='unique district')
        ]

class SubDistrictModel(TimeStampedModel):
    '''
    Holds District related Information
    '''
    subdistrictCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    subdistrictNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    subdistrictNameLocal = models.CharField(max_length=300,blank=True, null=True)
    districtCode = models.ForeignKey(DistrictModel, on_delete=models.CASCADE)
    stateCode = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    def __str__(self):
    # the self.subDistrictNameEnglish can be none so a empty string is attached
        return self.subdistrictNameEnglish + ""
    class Meta:
        constraints = [
            UniqueConstraint(fields=['subdistrictCode'], name='unique subdistrict')
        ]
    
    
class VillageModel(TimeStampedModel):
    '''
    Holds District related Information
    '''
    villageCode = models.IntegerField(blank=True, null=True)
    # census2001code = models.CharField(max_length=200,blank=True, null=True)
    # census2011code = models.CharField(max_length=200,blank=True, null=True)
    villageNameEnglish = models.CharField(max_length=300,blank=True, null=True)
    villageNameLocal = models.CharField(max_length=300,blank=True, null=True)
    subdistrictCode = models.ForeignKey(SubDistrictModel, on_delete=models.CASCADE)
    districtCode = models.ForeignKey(DistrictModel, on_delete=models.CASCADE)
    stateCode = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    def __str__(self):
    # the self.villageNameEnglish can be none so a empty string is attached
        return self.villageNameEnglish + ""
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['villageCode'], name='unique village')
        ]
