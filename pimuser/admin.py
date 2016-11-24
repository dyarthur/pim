from django.contrib import admin
from pimuser.models import PimUser, PimUserGroup

# Register your models here.
admin.site.register(PimUser)
admin.site.register(PimUserGroup)