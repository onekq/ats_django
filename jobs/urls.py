from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, UserRegistrationView, JobListView, JobDetailView
from .views import JobApplicationView, ApplicationStatusView, ApplicationDetailView, DashboardView
from .views import application_success, update_application_status

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('jobs/', JobListView.as_view(), name='jobs'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('apply/<int:job_id>/', JobApplicationView.as_view(), name='apply_for_job'),
    path('apply/', JobApplicationView.as_view(), name='apply'),
    path('application_success/<int:pk>/', application_success, name='application_success'),
    path('check_status/', ApplicationStatusView.as_view(), name='check_status'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('application/<uuid:application_number>/', ApplicationDetailView.as_view(), name='application_detail'),
    path('update_application_status/', update_application_status, name='update_application_status'),
    path('logout/', LogoutView.as_view(next_page='/jobs/login'), name='logout'),]
