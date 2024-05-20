from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import JobApplicationForm, ApplicationStatusForm
from .models import JobRequirement, JobApplication, Applicant
import random
import string

def generate_passcode(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

class JobApplicationView(View):
    def get(self, request, job_id):
        job_requirement = get_object_or_404(JobRequirement, id=job_id)
        form = JobApplicationForm(initial={'job_requirement': job_requirement})
        return render(request, 'apply.html', {'form': form, 'job_requirement': job_requirement})

    def post(self, request, job_id):
        job_requirement = get_object_or_404(JobRequirement, id=job_id)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            resume = form.cleaned_data['resume']

            applicant, created = Applicant.objects.get_or_create(email=email, defaults={'name': name, 'resume': resume})
            if not created:
                applicant.name = name
                applicant.resume = resume
                applicant.save()

            if JobApplication.objects.filter(applicant=applicant, job_requirement=job_requirement).exists():
                messages.error(request, 'You have already applied for this job.')
                return render(request, 'apply.html', {'form': form, 'job_requirement': job_requirement})

            job_application = JobApplication(
                applicant=applicant,
                job_requirement=job_requirement,
                status='Application Submitted',
                passcode=generate_passcode()
            )
            job_application.save()

            messages.success(request, 'Application submitted successfully!')
            return redirect('application_success', pk=job_application.pk)
        return render(request, 'apply.html', {'form': form, 'job_requirement': job_requirement})

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

class ApplicationDetailView(DetailView):
    model = JobApplication
    slug_field = 'application_number'
    slug_url_kwarg = 'application_number'
    template_name = 'application_detail.html'
