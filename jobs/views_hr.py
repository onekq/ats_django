from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import JobApplication, AuditLog

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

@login_required
def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'audit_log.html', {'logs': logs})