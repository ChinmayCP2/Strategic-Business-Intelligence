from django.contrib import admin
from .models import CatagoryModel,SummeryModel
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass
class SummeryAdmin(admin.ModelAdmin):
    pass


admin.site.register(CatagoryModel, AuthorAdmin)
admin.site.register(SummeryModel, SummeryAdmin)
