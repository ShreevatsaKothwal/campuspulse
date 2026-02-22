from django import forms
from .models import Complaint, Resource, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# ==========================
# Complaint Form
# ==========================

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['student_name', 'email', 'complaint_type', 'description']

        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'complaint_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3
            }),
        }


# ==========================
# Register Form
# ==========================

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
        }


# ==========================
# Login Form
# ==========================

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )


# ==========================
# Resource Form (STATIC VERSION)
# ==========================

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'category', 'year', 'file_name']  # ✅ file removed
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'year': forms.Select(attrs={'class': 'form-input'}),
            'file_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter file name (example: cyber_module_5.pdf)'
            }),
        }


# ==========================
# Discussion Forms
# ==========================

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }