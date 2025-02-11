from django.db import models
from users.models import EmployerProfile, JobSeekerProfile
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
#job category table
class JobCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_url = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "job_category"
        
#job posting Table
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
        ('Temporary', 'Temporary'),
        ('Remote', 'Remote'),
    ]
    
    SALARY_TYPE_CHOICES = [
        ('Hourly', 'Hourly'),
        ('Annual', 'Annual'),
        ('Monthly', 'Monthly'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('Entry-level', 'Entry-level'),
        ('Mid-level', 'Mid-level'),
        ('Senior-level', 'Senior-level'),
        ('Manager', 'Manager'),
        ('Director', 'Director'),
        ('Executive', 'Executive'),
        ('Intern', 'Intern'),
    ]
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE) #FK to employer_profile
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100)
    salary_type = models.CharField(max_length=100, choices=SALARY_TYPE_CHOICES, null=True, blank=True)
    job_type = models.CharField(max_length=100, choices=JOB_TYPE_CHOICES)
    requirements = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    experience_level = models.CharField(max_length=100, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True)
    application_instructions = models.TextField(null=True, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    company_logo = models.ImageField(upload_to="company_logos/",null=True, blank=True)
    featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def is_still_active(self):
        """Determines if the job is active based on the application deadline."""
        if not self.is_active:
            return False
        if self.application_deadline and self.application_deadline < timezone.now():
            return False
        return True
    def __atr__(self):
        return self.title
    
    class Meta:
        db_table = "job_posting"
        
# job Application Table
class JobApplication(models.Model):
    STATUS_CHOICES =(
        ('applied','Applied'),
        ('under_review','Under Review'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
    )
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE) # Fk to jobseeker profile
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE) # FK to JobPosting
    resume = models.FileField(upload_to="resumes/")
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Applied")
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.job_seeker.user.username} applied to {self.job.title}"
    
    class Meta:
        db_table = "job_application"
    
# Saved Jobs Table
class SavedJob(models.Model):
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE) #Fk to jobseeker profile
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE) #fk to jobposting
    saved_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job_seeker.user.username} saved {self.job.title}" 
    
    class Meta:
        db_table = "saved_job"
    
# Company Review Table
class CompanyReview(models.Model):
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE) # FK to jobseekerProfile
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE) # FK to EmployerProfile
    rating = models.IntegerField()
    review = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.job_seeker.user.username} for {self.company.company_name}" 
    class Meta:
        db_table = "company_review"       