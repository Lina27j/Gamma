from django.contrib import admin
from .models import CompanyProfile, ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'subject', 'submitted_at']
    list_filter   = ['submitted_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'submitted_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Contact',  {'fields': ['email', 'phone', 'address', 'working_hours']}),
        ('Catalogue', {'fields': ['catalogue']}),
        ('Map',      {'fields': ['map_link']}),
    ]

    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
