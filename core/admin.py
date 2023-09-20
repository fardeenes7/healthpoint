from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import *

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'speciality', 'bmdc', 'phone', 'consultation', 'followup', 'percentage')
    list_filter = ('name', 'degree', 'speciality', 'bmdc', 'phone', 'consultation', 'followup', 'percentage')
    search_fields = ('name', 'degree', 'speciality', 'bmdc', 'phone', 'consultation', 'followup', 'percentage')
    ordering = ['name']
admin.site.register(Doctor, DoctorAdmin)


admin.site.register(Speciality)
admin.site.register(Schedules)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)

admin.site.site_header = 'Healthpoint Admin Panel'
admin.site.site_title = 'Healthpoint Admin Panel'

admin.site.unregister(Group)
