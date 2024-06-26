from django.urls import path
from django.contrib.auth.views import LogoutView
from .views_auth import CustomLoginView, UserRegistrationView
from .views_jobs import home_redirect, JobListView, JobDetailView, CreateJobView, EditJobView
from .views_hr import DashboardView, update_application_status, audit_log_view
from .views_applications import ApplicationStatusView, ApplicationDetailView, JobApplicationView, application_success

urlpatterns = [
    path('', home_redirect, name='home'), 
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('jobs/', JobListView.as_view(), name='jobs'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', CreateJobView.as_view(), name='create_job'),
    path('jobs/edit/<int:job_id>/', EditJobView.as_view(), name='edit_job'),
    path('apply/<int:job_id>/', JobApplicationView.as_view(), name='apply'),
    path('application_success/<int:pk>/', application_success, name='application_success'),
    path('check_status/', ApplicationStatusView.as_view(), name='check_status'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('application/<uuid:application_number>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('update_application_status/', update_application_status, name='update_application_status'),
    path('audit_log/', audit_log_view, name='audit_log'),
    path('logout/', LogoutView.as_view(next_page='/jobs/login'), name='logout'),
]
