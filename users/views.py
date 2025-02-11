from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm, JobSeekerProfileForm, EmployerProfileForm,LoginForm
from django.contrib import messages
from users.models import EmployerProfile, JobSeekerProfile
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'index.html')

def employer_home(request):
    return render(request, 'users/employer_home.html')

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Save the user without committing to the database yet
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.set_password(user_form.cleaned_data['password1'])
            user.save() # Now save the user to the database
            
            # Determine user type and create corresponding profile
            user_type = user_form.cleaned_data['user_type']
            if user_type == 'employer':
                EmployerProfile.objects.create(user=user)
            elif user_type == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)
            
            messages.success(request, 'Registration successful ! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistrationForm() # Create an empty form for GET requests
    return render(request, 'users/registration.html', {'user_form':user_form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0) # Session will expire when the browser is closed
            
            login(request, user)
            
            print(f"Session data: {request.session.items()}")  # Print all session data
            print(f"User logged in: {user.username}")  # Print the logged-in user's username

            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            
            # redirect based on user type
            # Check if the user is an employer or job seeker and set user_type
            if EmployerProfile.objects.filter(user=user).exists():
                request.session['user_type'] = 'employer'
                messages.success(request, "Welcome!! you have logged in successfully.")
                return redirect('employer_home')
            elif JobSeekerProfile.objects.filter(user=user).exists():
                request.session['user_type'] = 'job_seeker'
                messages.success(request, "Welcome!! you have logged in successfully.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
                return redirect("user_login") # Default redirection if user type is unrecognized
    else:
        form = LoginForm()
    return render(request,"users/user_login.html",{"form":form})
  
def job_seeker_profile(request):
    user_id = request.session.get("user_id")
    
    if not user_id:
        messages.error(request, "please log in to access your profile.")
        return redirect("user_login")
    
    user = User.objects.get(id=user_id)
    profile, created = JobSeekerProfile.objects.get_or_create(user=user) # Get or create the profile
    
    if request.method == "POST":
        #update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email',user.email)
        user.save()
        
        # Update JobSeekerProfile fields
        profile.about = request.POST.get('about', profile.about)
        profile.address = request.POST.get('address', profile.address)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.skills = request.POST.get('skills', profile.skills)
        profile.experience = request.POST.get('experience', profile.experience)
        profile.education = request.POST.get('education', profile.education)
        profile.linkedin_url = request.POST.get('linkedin_url', profile.linkedin_url)
        profile.portfolio_url = request.POST.get('portfolio_url',profile.portfolio_url)
        profile.twitter_url = request.POST.get('twitter_url', profile.twitter_url)
        profile.instagram_url = request.POST.get('instagram_url',profile.instagram_url)
        profile.facebook_url = request.POST.get('facebook_url', profile.facebook_url)
        profile.resume = request.FILES.get('resume') or profile.resume
        profile.profile_image = request.FILES.get('profile_image') or profile.profile_image
        profile.save()
        
        messages.success(request, "Profile updated successfully.")
    return render(request, 'users/job_seeker_profile.html', {'user': user, 'profile': profile})


def employer_profile(request):
    user_id = request.session.get("user_id")
    
    if not user_id:
        messages.error(request, "Please log in to access your profile.")
        return redirect("user_login")
    
    user = User.objects.get(id=user_id)
    profile, created = EmployerProfile.objects.get_or_create(user=user) # Get or create the profile
       
    if request.method == "POST":
        # Update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        # Update EmployerProfile fields
        profile.company_name = request.POST.get('company_name', profile.company_name)
        profile.website = request.POST.get('company_website', profile.website)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.linkedin_url = request.POST.get('linkedin_url', profile.linkedin_url)
        profile.twitter_url = request.POST.get('twitter_url', profile.twitter_url)
        profile.facebook_url = request.POST.get('facebook_url', profile.facebook_url)
        profile.instagram_url = request.POST.get('instagram_url', profile.instagram_url)
        profile.about = request.POST.get('about', profile.about)
        profile.location = request.POST.get('location', profile.location)
        founded_date = request.POST.get('founded_date', profile.founded_date)
        if founded_date:
            profile.founded_date = founded_date 
       
        # Handle file upload for the company logo
        if 'logo' in request.FILES:
            profile.company_logo = request.FILES['logo']
            
        profile.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, 'users/employer_profile.html', {'user' : user, 'profile' : profile})
        
def user_logout(request):   
    request.session.flush()
    messages.success(request, "you have successfully logged out.") 
    return redirect("home")
