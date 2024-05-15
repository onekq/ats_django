from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobApplication, Applicant

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['email', 'name', 'resume', 'contact_information']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant', 'job_requirement']

class ApplicationStatusForm(forms.Form):
    job_req_id = forms.IntegerField()
    passcode = forms.CharField(max_length=20)
