from django.contrib import admin
from .models import JobRequirement, Applicant, JobApplication, User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

@admin.register(JobRequirement)
class JobRequirementAdmin(admin.ModelAdmin):
    list_display = ('department', 'function', 'rank')
    search_fields = ('department', 'function', 'rank')
    ordering = ('department', 'function', 'rank')

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_number', 'applicant', 'job_requirement', 'status', 'passcode')
    search_fields = ('application_number', 'applicant__name', 'job_requirement__department')
    ordering = ('application_number',)

admin.site.register(User, CustomUserAdmin)
