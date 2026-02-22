from django.contrib import admin
from .models import Complaint, Resource, Post, Comment


# ==========================
# Complaint Admin
# ==========================

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'email',
        'complaint_type',
        'status',
        'created_at'
    )

    list_filter = (
        'complaint_type',
        'status',
        'created_at'
    )

    search_fields = (
        'student_name',
        'email',
        'description'
    )

    ordering = ('-created_at',)


# ==========================
# Resource Admin (FIXED)
# ==========================

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'uploaded_at')  # removed file
    list_filter = ('category', 'year', 'uploaded_at')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)


# ==========================
# Discussion Models
# ==========================

admin.site.register(Post)
admin.site.register(Comment)