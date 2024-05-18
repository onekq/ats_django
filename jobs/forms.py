from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobApplication, JobRequirement, Applicant

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['email', 'name', 'resume', 'contact_information']

class JobApplicationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100, required=True)
    resume = forms.FileField(required=True)

    class Meta:
        model = JobApplication
        fields = ['job_requirement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_requirement'].queryset = JobRequirement.objects.all()

class ApplicationStatusForm(forms.Form):
    job_req_id = forms.CharField()
    passcode = forms.CharField(max_length=20)

class JobRequirementForm(forms.ModelForm):
    class Meta:
        model = JobRequirement
        fields = ['department', 'function', 'rank', 'description']
