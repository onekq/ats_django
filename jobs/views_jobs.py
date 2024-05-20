from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib import messages
from .models import JobRequirement
from .forms import JobRequirementForm

def home_redirect(request):
    return redirect('jobs')

class JobListView(View):
    def get(self, request):
        job_requirements = JobRequirement.objects.all()
        return render(request, 'jobs.html', {'job_requirements': job_requirements})

class JobDetailView(DetailView):
    model = JobRequirement
    template_name = 'job_detail.html'
    context_object_name = 'job_requirement'

class CreateJobView(View):
    def get(self, request):
        form = JobRequirementForm()
        return render(request, 'create_job.html', {'form': form})

    def post(self, request):
        form = JobRequirementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job created successfully!')
            return redirect('jobs')
        return render(request, 'create_job.html', {'form': form})

class EditJobView(View):
    def get(self, request, job_id):
        job = get_object_or_404(JobRequirement, id=job_id)
        form = JobRequirementForm(instance=job)
        return render(request, 'edit_job.html', {'form': form, 'job': job})

    def post(self, request, job_id):
        job = get_object_or_404(JobRequirement, id=job_id)
        form = JobRequirementForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs')
        return render(request, 'edit_job.html', {'form': form, 'job': job})
