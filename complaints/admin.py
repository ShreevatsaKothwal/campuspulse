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
# Resource Admin (Static Version)
# ==========================

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'year',
        'file_name',
        'uploaded_at'
    )

    list_filter = (
        'category',
        'year',
    )

    search_fields = (
        'title',
    )

    ordering = ('-uploaded_at',)


# ==========================
# Discussion Models
# ==========================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_by', 'created_at')
    ordering = ('-created_at',)