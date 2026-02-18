# from django.contrib import admin
# from .models import Complaint
#
# admin.site.register(Complaint)
from django.contrib import admin
from .models import Complaint
from django.contrib import admin
from .models import Complaint, Resource
from .models import Post, Comment



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


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'uploaded_at', 'uploaded_by')
    list_filter = ('category', 'year', 'uploaded_at')
    fields = ('title', 'category', 'year', 'file', 'uploaded_by')

    search_fields = (
        'title',
    )

    ordering = ('-uploaded_at',)

    admin.site.register(Post)
    admin.site.register(Comment)














