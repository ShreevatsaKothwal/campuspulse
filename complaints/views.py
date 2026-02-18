from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import ResourceForm
from .models import Complaint, Resource
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
import re
from .models import Complaint
from .forms import ComplaintForm, RegisterForm, LoginForm

# ----------------------------------------------------------------------------------------------------
def home(request):

    ppt_resources = Resource.objects.filter(category='PPT').order_by('-uploaded_at')
    question_resources = Resource.objects.filter(category='Question Paper').order_by('-uploaded_at')
    notes_resources = Resource.objects.filter(category='Notes').order_by('-uploaded_at')
    latest_posts = Post.objects.all().order_by('-created_at')[:3]


    context = {
        'ppt_resources': ppt_resources,
        'question_resources': question_resources,
        'notes_resources': notes_resources,
        'latest_posts': latest_posts,
    }

    return render(request, 'home.html', context)

# ----------------------------------------------------------------------------------------------------




def generate_summary(complaint_type, description):
    # Clean spacing
    description = re.sub(r'\s+', ' ', description).strip()

    # Normalize text
    description = description.capitalize()

    # Detect urgency keywords
    urgent_keywords = ["urgent", "immediately", "asap", "serious", "critical"]
    severity_keywords = ["bad", "worst", "poor", "not good", "problem", "issue"]

    urgency_flag = any(word in description.lower() for word in urgent_keywords)
    severity_flag = any(word in description.lower() for word in severity_keywords)

    # Extract first 30 words safely
    words = description.split()
    short_text = " ".join(words[:30])

    # Structured professional summary
    summary = (
        f"A student from Dayananda Sagar University has raised a complaint under the "
        f"{complaint_type} category. The primary concern highlighted is: {short_text}."
    )

    if severity_flag:
        summary += " The issue appears to significantly affect the student experience."

    if urgency_flag:
        summary += " Immediate administrative attention may be required."

    return summary


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user

            # Generate AI Summary
            summary = generate_summary(
                complaint.complaint_type,
                complaint.description
            )

            complaint.summary = summary  # Save summary in model
            complaint.save()

            # Send Email Automatically
            send_mail(
                subject=f"New Complaint - {complaint.complaint_type}",
                message=f"""
New Complaint Received:

Student Name: {complaint.student_name}
Student Email: {complaint.email}
Category: {complaint.complaint_type}

Summary:
{summary}

Full Description:
{complaint.description}
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.DEAN_EMAIL],
                fail_silently=False,
            )

            return render(request, 'success.html')

    else:
        form = ComplaintForm()

    return render(request, 'submit_complaint.html', {'form': form})


@login_required
def complaint_list(request):
    complaint_type = request.GET.get('type')
    status_filter = request.GET.get('status')

    # Base queryset
    if request.user.is_superuser:
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(user=request.user)

    # Category filter
    if complaint_type:
        complaints = complaints.filter(complaint_type=complaint_type)

    # Status filter (admin only)
    if request.user.is_superuser and status_filter:
        complaints = complaints.filter(status=status_filter)

    complaints = complaints.order_by('-created_at')

    # Pagination
    paginator = Paginator(complaints, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'complaints': page_obj,
        'selected_type': complaint_type,
        'selected_status': status_filter,
        'page_obj': page_obj
    }

    return render(request, 'complaint_list.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    message = None

    if not request.user.is_authenticated and request.GET.get('next'):
        message = "Please login first to access that page."

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'message': message
    })


def user_logout(request):
    logout(request)
    return redirect('home')


from django.shortcuts import get_object_or_404
@login_required
def update_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.user.is_superuser:

        # Toggle status
        if complaint.status == "Pending":
            complaint.status = "Resolved"
        else:
            complaint.status = "Pending"

        complaint.save()

        # 🔥 Send Email to Student
        send_mail(
            subject="Update on Your Complaint – CampusPulse",
            message=f"""
Dear {complaint.student_name},

Your complaint submitted under the {complaint.complaint_type} category has been updated.

Current Status: {complaint.status}

Summary:
{complaint.summary}

If the issue persists, you may submit a new complaint through CampusPulse.

Regards,
CampusPulse Team
Dayananda Sagar University
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[complaint.email],
            fail_silently=False,
        )

    return redirect('complaint_list')


#
# from django.core.mail import send_mail
# from django.conf import settings
# from django.http import HttpResponse
#
# def test_email(request):
#     send_mail(
#         subject='CampusPulse Test Email',
#         message='This is a test email from CampusPulse project.',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[settings.DEAN_EMAIL],
#         fail_silently=False,
#     )
#     return HttpResponse("Test email sent successfully!")

from django.db.models import Count

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status='Pending').count()
    resolved_complaints = Complaint.objects.filter(status='Resolved').count()
    hostel_complaints = Complaint.objects.filter(complaint_type='Hostel').count()
    bus_complaints = Complaint.objects.filter(complaint_type='Bus').count()

    context = {
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'hostel_complaints': hostel_complaints,
        'bus_complaints': bus_complaints,
    }

    return render(request, 'admin_dashboard.html', context)

@login_required
def upload_resource(request):

    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('home')
    else:
        form = ResourceForm()

    return render(request, 'upload_resource.html', {'form': form})

def resource_category(request, category):

    selected_year = request.GET.get('year')
    resources = None  # default

    if selected_year:
        resources = Resource.objects.filter(
            category=category,
            year=selected_year
        ).order_by('-uploaded_at')

    context = {
        "resources": resources,
        "category": category,
        "selected_year": selected_year,
    }

    return render(request, "resource_category.html", context)






@login_required
def discussion_list(request):
    posts_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts_list, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'discussion_list.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('discussion_list')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }

    return render(request, 'post_detail.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_superuser:
        post.delete()

    return redirect('discussion_list')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id

    if request.user.is_superuser:
        comment.delete()

    return redirect('post_detail', post_id=post_id)
