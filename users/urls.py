from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('employer/home/', views.employer_home, name='employer_home'),
    path('profile/job_seeker/', views.job_seeker_profile, name='job_seeker_profile'),
    path('profile/employer/', views.employer_profile, name='employer_profile'),
    path('logout/', views.user_logout, name='logout'),
]