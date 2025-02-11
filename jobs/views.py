from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from jobs.models import JobPosting, JobCategory, JobApplication, SavedJob
from users.models import EmployerProfile, JobSeekerProfile
from django.utils import timezone
# Create your views here.
def job_posting(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'employer':
        if 'user_id' not in request.session:
            messages.error(request, "Please log in to post a job.")
            return redirect('login') # Redirect to the login page if not logged in
        else:
            messages.error(request, "please log in as an employer to post a job.")
            return redirect('login') # redirect to the home page if looged in as a non-employer
    
    employer_profile = EmployerProfile.objects.get(user=request.user)   
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        location = request.POST["location"]
        is_remote = request.POST.get("is_remote")  # Check if remote is selected
        salary = request.POST["salary"]
        salary_type = request.POST["salary_type"]
        job_type = request.POST["job_type"]
        requirements = request.POST["requirements"]
        skills = request.POST["skills"]
        benefits = request.POST["benefits"]
        experience_level = request.POST["experience_level"]
        application_instructions = request.POST["application_instructions"]
        application_deadline = request.POST["application_deadline"]
        category_name = request.POST["category_name"]
        category_description = request.POST["category_description"]
        is_active = request.POST["is_active"] == "1"  # Employment Status
        
        
        # Handle remote location logic
        location = "Remote" if is_remote else location or "Not specified"
        
        #handle category
        category_id = request.POST.get("category")
        if category_id:  # If an existing category is selected from the dropdown
            category = JobCategory.objects.get(id=category_id)
            messages.success(request, f"Category '{category.name}' selected.")
        else:  # If a new category is entered
            category, created = JobCategory.objects.get_or_create(name=category_name, defaults={'description': category_description})
            if not created:
                # If category already exists, display warning and stop job posting creation
                messages.warning(request, "Category already exists. Please choose from the list.")
                return redirect('job_posting')  # Redirect back to form to allow correction
            else:
                messages.success(request, f"New category '{category_name}' added!")
                
        # Create Job Posting
        job_posting = JobPosting(
            employer = EmployerProfile.objects.get(user=request.user),
            category = category,
            title = title,
            description = description,
            location = location,
            salary = salary,
            salary_type = salary_type,
            job_type=job_type,
            requirements = requirements,
            skills= skills,
            benefits = benefits,
            experience_level = experience_level,
            application_instructions = application_instructions,
            application_deadline = application_deadline,
            is_active = is_active,
            company_logo= employer_profile.company_logo 
        )
        job_posting.save()
        messages.success(request, "Job posted successfully!")
        return redirect('employer_job_list')
    
    salary_type_choices = JobPosting.SALARY_TYPE_CHOICES
    job_type_choices = JobPosting.JOB_TYPE_CHOICES
    experience_level_choices = JobPosting.EXPERIENCE_LEVEL_CHOICES
    
    # get company information from employer profile
    employer_profile = EmployerProfile.objects.get(user=request.user)
    categories = JobCategory.objects.all() # Fetch all categories
    
    return render(request, "jobs/job_posting.html", {"employer_profile":employer_profile, "categories":categories,  "salary_type_choices": salary_type_choices,  "job_type_choices": job_type_choices, "experience_level_choices": experience_level_choices, })

def employer_job_list(request):
    #check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session['user_type'] != 'employer':
        messages.error(request, "please log in as an employer to view your job postings")
        return redirect('login')
    
    #get the looged-in employer's profile and their job postings
    employer = EmployerProfile.objects.get(user=request.user)
    job_postings = JobPosting.objects.filter(employer=employer)
    
    for job in job_postings:
        job.requirements_list = job.requirements.split("; ") if job.requirements else []
    
    return render(request, "jobs/employer_job_list.html", {"job_posting":job_postings})


def edit_job_posting(request, job_id):
    #check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session['user_type'] != 'employer':
        messages.error(request, "Please log in as an employer to edit the job posting.")
        return redirect('login')
    
    employer_profile = EmployerProfile.objects.get(user=request.user)
    job_posting = get_object_or_404(JobPosting, id=job_id, employer=employer_profile)
    
    if request.method == "POST":
        # Update the job fields from the POST data
        job_posting.title = request.POST['title']
        job_posting.description = request.POST['description']
        job_posting.location = "Remote" if request.POST.get('is_remote') else request.POST['location']
        job_posting.salary = request.POST['salary']
        job_posting.salary_type = request.POST['salary_type']
        job_posting.job_type = request.POST['job_type']
        job_posting.requirements = request.POST['requirements']
        job_posting.skills = request.POST['skills']
        job_posting.benefits = request.POST['benefits']
        job_posting.experience_level = request.POST['experience_level']
        job_posting.application_instructions = request.POST['application_instructions']
        job_posting.is_active = request.POST.get('is_active') == '1'
        
         # Handle category selection or creation
        category_id = request.POST.get("category")
        category_name = request.POST["category_name"]
        category_description = request.POST["category_description"]
        
        if category_id:  # If an existing category is selected from the dropdown
            category = JobCategory.objects.get(id=category_id)
            messages.success(request, f"Category '{category.name}' selected.")
        else:  # If a new category is entered
            category, created = JobCategory.objects.get_or_create(
                name=category_name, 
                defaults={'description': category_description}
            )
            if not created:
                # If category already exists, display warning and stop job posting update
                messages.warning(request, "Category already exists. Please choose from the list.")
                return redirect('edit_job_posting', job_id=job_id)  # Redirect back to form
            else:
                messages.success(request, f"New category '{category_name}' added!")

        # Assign the selected or newly created category to the job posting
        job_posting.category = category
        #save updated job posting
        job_posting.updated_at = timezone.now()
        job_posting.save()
        
        messages.success(request, "job posting updated successfully!")
        return redirect('employer_job_list')
    
    salary_type_choices = JobPosting.SALARY_TYPE_CHOICES
    job_type_choices = JobPosting.JOB_TYPE_CHOICES
    experience_level_choices = JobPosting.EXPERIENCE_LEVEL_CHOICES
    categories = JobCategory.objects.all()
    
    context = {
        'job_posting':job_posting,
        'categories': categories,
        'salary_type_choices': salary_type_choices,
        'job_type_choices': job_type_choices,
        'experience_level_choices': experience_level_choices,
    }
    return render(request, 'jobs/edit_job_posting.html', context)

def delete_job_posting(request, job_id):
    # check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session['user_type'] != 'employer':
        messages.error(request, "Please log in as an employer to delete the job.")
        return redirect('login')
    
    employer_profile = EmployerProfile.objects.get(user=request.user)
    job_posting = get_object_or_404(JobPosting, id=job_id, employer=employer_profile)
    
    if request.method == "POST":
        job_posting.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('employer_job_list')
    
    return redirect('employer_job_list')

def close_job_posting(request, job_id):
    # check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session['user_type'] != 'employer':
        messages.error(request, "Please log in as an employer to close the job.")
        return redirect('login')
    employer_profile = EmployerProfile.objects.get(user=request.user)
    job_posting = get_object_or_404(JobPosting, id=job_id, employer = employer_profile)
    # check job_status
    if not job_posting.is_active:
        print("POST request received, closing job...")
        messages.info(request, "This job is already closed.")
        return redirect('employer_job_list')
    
    if request.method == "POST":
        job_posting.is_active = False
        job_posting.save()
        messages.success(request, "Job closed successfully!")
        return redirect('employer_job_list')
    return redirect('employer_job_list')

def job_seeker_job_list(request):
    #get all active job postings
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True) # it will show only active jobs
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
    
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings": job_postings,"employer":employer})

def job_seeker_internship_job(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Internship')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})
        
def job_seeker_full_time(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Full-time')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})
        
def job_seeker_part_time(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Part-time')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})

def job_seeker_contract_job(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Contract')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})

def job_seeker_remote_job(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Remote')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})

def job_seeker_temporary_job(request):
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(is_active=True, job_type='Temporary')
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer})
        
def apply_job(request, job_id):
    #check if the user is logged in and is a job seeker
    if 'user_id' not in request.session or request.session.get('user_type') != 'job_seeker':
        messages.error(request, "Please log in as a job seeker to apply for this job.")
        return redirect('login')
    
    job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    job_posting = get_object_or_404(JobPosting, id=job_id, is_active=True)
    
    
     # Split requirements and skills into lists for easier display
    job_posting.requirements_list = job_posting.requirements.split(";") if job_posting.requirements else []
    job_posting.skills_list = job_posting.skills.split(";") if job_posting.skills else []
    
    #check if job seeker has already applied to this job
    if JobApplication.objects.filter(job_seeker = job_seeker_profile, job=job_posting).exists():
        messages.info(request,"you have already applied to this job")
        return redirect('job_seeker_job_list')
    
    #check if mandatory fields are missing in JobSeekerProfile
    incomplete_profile = not all([job_seeker_profile.phone_number, job_seeker_profile.address, job_seeker_profile.education, job_seeker_profile.experience, job_seeker_profile.skills, job_seeker_profile.about])
    
    if request.method == "POST":
        # if profile is incomplete, update it with provided data
        if incomplete_profile:
            job_seeker_profile.phone_number = request.POST['phone_number']
            job_seeker_profile.address = request.POST['address']
            job_seeker_profile.education = request.POST['education']
            job_seeker_profile.experience = request.POST['experience']
            job_seeker_profile.about = request.POST['about']
            job_seeker_profile.skills = request.POST['skills']
            job_seeker_profile.save()
            messages.success(request, "Profile updated successfully. you can now apply for this job.")
            return redirect('apply_job',job_id=job_id)
        
        # If profile is complete, proceed with job application
        resume_file = request.FILES.get('resume')
        if resume_file or job_seeker_profile.resume:
            #save new resume to both JobSeekerProfile and JobApplication
            if resume_file:
                job_seeker_profile.resume.save(resume_file.name, resume_file)
                job_seeker_profile.save()
                
            #create a new job application
            job_application = JobApplication(job_seeker = job_seeker_profile, job=job_posting,resume=resume_file or job_seeker_profile.resume,applied_date=timezone.now())
            job_application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('job_seeker_job_list')
        else:
            messages.error(request, "Please upload a resume to apply for this job.")
            return redirect('apply_job',job_id=job_id)
        
    return render(request, 'jobs/apply_job.html',{'job_posting':job_posting,'incomplete_profile': incomplete_profile,'job_seeker_profile': job_seeker_profile,'existing_resume':job_seeker_profile.resume.url if job_seeker_profile.resume else None})

def applied_jobs(request):
    # check if the user is logged in and is a job seeker
    if 'user_id' not in request.session or request.session.get('user_type') != 'job_seeker':
        messages.error(request, "Please log in as a job seeker to view your applied jobs.")
        return redirect('login')
    
    #Fetch the job seeker profile
    try:
        job_seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, "Your profile is incomplete. Please complete your profile to view applied jobs.")
    
    # Retrive the list of applied jobs.
    applied_jobs_list = JobApplication.objects.filter(job_seeker=job_seeker_profile).select_related('job').order_by('-applied_date')
    
    return render(request, 'jobs/applied_jobs.html', {'applied_jobs_list':applied_jobs_list, 'job_seeker_profile':job_seeker_profile,})
 
def withdraw_application(request, application_id):
    if 'user_id' not in request.session or request.session['user_type'] != 'job_seeker':
        messages.error(request, "You need to log in as a job seeker to withdraw an application.")
        return redirect('login')
    
    application = get_object_or_404(JobApplication, id=application_id, job_seeker__user_id=request.session['user_id'])
    
    #withdraw the application
    application.delete()
    messages.success(request, "you have successfully withdrawn your application.")
    return redirect('job_seeker_job_list')
       
def job_detail(request, job_id):
    # Fetch the specific job posting
    job_posting = get_object_or_404(JobPosting, id=job_id)
    
    # Parse requirements and skills into lists for display
    job_posting.requirements_list = job_posting.requirements.split(";") if job_posting.requirements else []
    job_posting.skills_list = job_posting.skills.split(";") if job_posting.skills else []
    job_posting.benefits_list = job_posting.benefits.split(";") if job_posting.benefits else []
    
    employer = EmployerProfile.objects.get(user=job_posting.employer.user)
    
    # Determine user type
    user_type = request.session.get('user_type')
    
    # Handle logic for job seeker
    if user_type == 'job_seeker':
        job_seeker_profile = JobSeekerProfile.objects.get(user = request.user)
        has_applied = JobApplication.objects.filter(job_seeker=job_seeker_profile, job=job_posting).exists()
        context = {
            'job_posting': job_posting,
            'employer': employer,
            'is_job_seeker': True,
            'has_applied': has_applied,
        }
    
    # Handle logic for employer
    elif user_type == 'employer':
        employer_profile = EmployerProfile.objects.get(user=request.user)
        is_owner = (job_posting.employer == employer_profile)
        context = {
            'job_posting': job_posting,
            'employer': employer,
            'is_employer': True,
            'is_owner': is_owner,
        }
    # For non-logged-in users or unknown user type
    else:
        context = {
            'job_posting': job_posting,
            'employer': employer,
        }
    
    return render(request, 'jobs/job_detail.html', context)

def save_job(request, job_id):
    if 'user_id' not in request.session or request.session['user_type'] != 'job_seeker':
        messages.error(request, "Please log in as a job seeker to save jobs.")
        return redirect('login')
    
    job_seeker = get_object_or_404(JobSeekerProfile, user=request.user)
    job = get_object_or_404(JobPosting , id=job_id, is_active=True)
    
    if SavedJob.objects.filter(job_seeker=job_seeker, job=job).exists():
        messages.info(request, "You have already saved this job.")
    else:
        # save the job
        SavedJob.objects.create(job_seeker=job_seeker, job=job)
        messages.success(request, "Job has been saved successfully!")
    
    return redirect('job_detail', job_id=job_id)

def saved_jobs_list(request):
    if 'user_id' not in request.session or request.session['user_type'] != 'job_seeker':
        messages.error(request, "Please log in as a job seeker to view saved jobs.")
        return redirect('login')
    
    job_seeker = get_object_or_404(JobSeekerProfile, user=request.user)
    saved_jobs = SavedJob.objects.filter(job_seeker=job_seeker)
    
    return render(request, 'jobs/saved_jobs.html',{'saved_jobs':saved_jobs})

def remove_saved_job(request, job_id):
    if 'user_id' not in request.session or request.session['user_type'] != 'job_seeker':
        messages.error(request, "Please log in as a job seeker to manage saved jobs.")
        return redirect('login')
    
    job_seeker = get_object_or_404(JobSeekerProfile, user=request.user)
    job = get_object_or_404(JobPosting, id=job_id)
    
    #check if the job is saved by the user
    saved_job = SavedJob.objects.filter(job_seeker=job_seeker, job=job).first()
    if saved_job:
        saved_job.delete()
        messages.success(request, "Job has been removed from your saved list.")
    else:
        messages.error(request, "This job is not in your saved list.")
    return redirect('saved_jobs')

def manage_applications(request):
    # check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session.get('user_type') != 'employer':
        messages.error(request, "Please log in as an employer to manage applications.")
        return redirect("login")
    
    try:
        #get the employer's profile
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        messages.error(request, "your employer profile is incomplete.")
        return redirect('employer_dashboard')
    
    # get all job applications for jobs posted by this employer
    applications = JobApplication.objects.filter(job__employer=employer_profile).select_related('job', 'job_seeker').order_by('-applied_date')
    
    return render(request, "jobs/manage_applications.html",{"applications":applications})

def application_detail(request, application_id):
    # check if the user is logged in and is an employer
    if 'user_id' not in request.session or request.session.get('user_type') != 'employer':
        messages.error(request, "please log in as an employer to view application details.")
        return redirect('login')
    
    application = get_object_or_404(JobApplication, id=application_id, job__employer__user_id=request.session['user_id'])
    
    if request.method == "POST":
        # update application status
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, "Application status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect('manage_applications')
    
    return render(request, 'jobs/application_detail.html',{'application':application})

def category_wise_jobs(request, category_id):
    category = get_object_or_404(JobCategory, id=category_id)
    # filter job postings to show only active jobs of type internship
    employer = EmployerProfile.objects.all()
    job_postings = JobPosting.objects.filter(category=category, is_active=True)
    
    # split requirements into a list for display purpose
    for job in job_postings:
        job.requirements_list = job.requirements.split(";") if job.requirements else []
        
    return render(request, "jobs/job_seeker_job_list.html", {"job_postings":job_postings, 'employer':employer,  'category': category})
    