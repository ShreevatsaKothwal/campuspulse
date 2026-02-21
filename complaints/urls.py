from django.urls import path
from . import views
# from .views import test_email
from .views import admin_dashboard
from .views import upload_resource



urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    # path('test-email/', test_email, name='test_email'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('upload-resource/', upload_resource, name='upload_resource'),
    path('static/<str:category>/', views.resource_category, name='resource_category'),

    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/create/', views.create_post, name='create_post'),
    path('discussions/<int:post_id>/', views.post_detail, name='post_detail'),
    path('discussions/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),


]



