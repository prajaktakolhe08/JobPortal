from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #linked to built-in user
    resume = models.FileField(upload_to='resumes/',null=True,blank=True)
    skills = models.TextField(null=True,blank=True)
    experience = models.TextField(null=True,blank=True)
    education = models.TextField(null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile_images/',null=True, blank=True)
    linkedin_url = models.URLField(null=True,blank=True)
    portfolio_url = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True,blank=True)
    twitter_url = models.URLField(null=True,blank=True)
    facebook_url = models.URLField(null=True,blank=True)
    instagram_url = models.URLField(null=True,blank=True) 
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "job_seeker_profile"
        
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #linked to built-in user
    company_name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    company_logo = models.ImageField(upload_to="company_logos/",null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    founded_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=255)
    linkedin_url = models.URLField(null=True,blank=True)
    twitter_url = models.URLField(null=True,blank=True)
    facebook_url = models.URLField(null=True,blank=True)
    instagram_url = models.URLField(null=True,blank=True) 
    phone_number = models.CharField(max_length=15, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = "employer_profile"      