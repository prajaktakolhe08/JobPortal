from django.contrib import admin
from .models import JobCategory, JobPosting, JobApplication, SavedJob, CompanyReview

# Register your models here.

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','created_at','updated_at')
    search_fields = ('name',)
    
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('id','title','employer','category','location','salary','salary_type','job_type','experience_level','application_deadline','is_active','featured','posted_date','is_active')
    search_fields = ('title', 'employer__username', 'category__name', 'location')
    list_filter = ('job_type', 'is_active', 'posted_date')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'applied_date', 'status')
    search_fields = ('job_seeker__username', 'job__title', 'status')
    list_filter = ('status',)
    
@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'job', 'saved_date')
    search_fields = ('job_seeker__username', 'job__title')
    
@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'company', 'rating', 'review_date')
    search_fields = ('job_seeker__username', 'company__company_name')
    list_filter = ('rating',)
