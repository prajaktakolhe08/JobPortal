from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import JobSeekerProfile, EmployerProfile
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name','last_name','user_type','phone_number','address','password1','password2')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adding placeholders to each field
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter a unique username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your email address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name'})
        self.fields['user_type'].widget.attrs.update({'placeholder': 'Select user type'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Your phone number'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Your address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        
        # Remove help text from all fields
        for field in self.fields.values():
            field.help_text = None  
            
class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Remember Me")
        
class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume','skills','experience','education','profile_image','linkedin_url','portfolio_url']
        
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name','website','company_logo','about','founded_date','location','linkedin_url','twitter_url','facebook_url','instagram_url']