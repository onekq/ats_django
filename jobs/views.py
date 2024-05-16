from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, ApplicantForm, JobApplicationForm, ApplicationStatusForm
from .models import JobRequirement, JobApplication, Applicant
import random
import string
import json

def generate_passcode(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')

class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User created:", user)
            login(request, user)
            return redirect('dashboard')
        print("Form errors:", form.errors)
        return render(request, 'register.html', {'form': form})

class JobApplicationView(View):
    def get(self, request):
        form = JobApplicationForm()
        return render(request, 'apply.html', {'form': form})

    def post(self, request):
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            resume = form.cleaned_data['resume']
            job_requirement = form.cleaned_data['job_requirement']

            applicant, created = Applicant.objects.get_or_create(email=email, defaults={'name': name, 'resume': resume})
            if not created:
                applicant.name = name
                applicant.resume = resume
                applicant.save()

            if JobApplication.objects.filter(applicant=applicant, job_requirement=job_requirement).exists():
                messages.error(request, 'You have already applied for this job.')
                return render(request, 'apply.html', {'form': form})

            job_application = JobApplication(
                applicant=applicant,
                job_requirement=job_requirement,
                status='Application Submitted',
                passcode=generate_passcode()
            )
            job_application.save()

            messages.success(request, 'Application submitted successfully!')
            return redirect('application_success', pk=job_application.pk)
        return render(request, 'apply.html', {'form': form})

def application_success(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'application_success.html', {'job_application': job_application})

class ApplicationStatusView(View):
    def get(self, request):
        form = ApplicationStatusForm()
        return render(request, 'check_status.html', {'form': form})

    def post(self, request):
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            job_req_id = form.cleaned_data['job_req_id']
            passcode = form.cleaned_data['passcode']
            try:
                application = JobApplication.objects.get(application_number=job_req_id, passcode=passcode)
                return render(request, 'application_detail.html', {'application': application})
            except JobApplication.DoesNotExist:
                form.add_error(None, 'Invalid Job Req ID or Passcode')
        return render(request, 'check_status.html', {'form': form})

class DashboardView(View):
    def get(self, request):
        applications = JobApplication.objects.all()
        statuses = [
            "Application Submitted", 
            "Phone screen offered", 
            "Phone screen complete", 
            "On-site offered", 
            "Offer", 
            "Hired"
        ]
        
        # Debugging: print the applications and their statuses to the console
        for application in applications:
            print(f"Application: {application} Status: {application.status}")
        
        return render(request, 'dashboard.html', {'applications': applications, 'statuses': statuses})

class ApplicationDetailView(DetailView):
    model = JobApplication
    slug_field = 'application_number'
    slug_url_kwarg = 'application_number'
    template_name = 'application_detail.html'

@csrf_exempt
def update_application_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        application_number = data.get('application_number')
        new_status = data.get('status')

        try:
            application = JobApplication.objects.get(application_number=application_number)
            application.status = new_status
            application.save()
            return JsonResponse({'success': True})
        except JobApplication.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Application not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
