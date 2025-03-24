from django.contrib import admin
from accounts import models as accounts_models

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'date']

admin.site.register(accounts_models.User, UserAdmin)
admin.site.register(accounts_models.Profile, ProfileAdmin)
admin.site.register(accounts_models.ContactMessage, ContactMessageAdmin)
    