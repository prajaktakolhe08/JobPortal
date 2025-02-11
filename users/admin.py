from django.contrib import admin
from .models import JobSeekerProfile, EmployerProfile

# Register your models here.

class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','resume','skills','experience','education','created_at','updated_at')
    search_fields = ('user__username', 'skills', 'experience')

class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','company_name','website','location','created_at','updated_at')
    search_fields = ('user__username', 'company_name', 'location')

admin.site.register(JobSeekerProfile,JobSeekerProfileAdmin)
admin.site.register(EmployerProfile,EmployerProfileAdmin)



