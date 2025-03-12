from django.contrib import admin
from .models import Profile , CustomUser
# Register your models here.



admin.site.register(CustomUser)
admin.site.register(Profile)