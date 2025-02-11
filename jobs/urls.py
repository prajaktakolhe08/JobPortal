from django.urls import path
from . import views

urlpatterns = [
    path('job_posting/', views.job_posting, name='job_posting'),
    path('my-jobs/',views.employer_job_list, name='employer_job_list'),
    path('edit-job/<int:job_id>/', views.edit_job_posting, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job_posting, name='delete_job'),
    path('close-job/<int:job_id>/', views.close_job_posting, name='close_job'),
    path('job-seeker/job-list/',views.job_seeker_job_list, name='job_seeker_job_list'),
    path('apply_job/<int:job_id>/',views.apply_job,name='apply_job'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
    path('job-detail/<int:job_id>/',views.job_detail, name='job_detail'),
    path('withdraw-application/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('save_job/<int:job_id>/',views.save_job, name='save_job'),
    path('saved_jobs/',views.saved_jobs_list, name='saved_jobs'),
    path('remove_saved_job/<int:job_id>/', views.remove_saved_job, name='remove_saved_job'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('internship-jobs/', views.job_seeker_internship_job, name='job_seeker_internship_job'),
    path('contract-jobs/', views.job_seeker_contract_job, name='job_seeker_contract_job'),
    path('temporary-jobs/', views.job_seeker_temporary_job, name='job_seeker_temporary_job'),
    path('part-time-jobs/', views.job_seeker_part_time, name='job_seeker_part_time'),
    path('full-time-jobs/', views.job_seeker_full_time, name='job_seeker_full_time'),
    path('remote-jobs/', views.job_seeker_remote_job, name='job_seeker_remote_job'),
    path('category/<int:category_id>/', views.category_wise_jobs, name='category_jobs'),
]