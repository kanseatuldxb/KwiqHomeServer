from django.contrib import admin
# Register your models here.
from .models import Organization, Employee

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    search_fields = ['name']
    list_filter = ['created_at', 'updated_at']

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['email', 'organization', 'user_type', 'created_at', 'updated_at']
    search_fields = ['email', 'organization', 'user_type']
    list_filter = ['created_at', 'updated_at']




admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)