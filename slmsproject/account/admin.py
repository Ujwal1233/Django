from django.contrib import admin
from .models import LeaveRequest, Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'role')
	search_fields = ('user__username', 'role')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
	list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
	list_filter = ('status', 'leave_type', 'created_at')
	search_fields = ('user__username', 'reason', 'admin_comment')
