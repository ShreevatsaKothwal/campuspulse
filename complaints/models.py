from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    COMPLAINT_CHOICES = [
        ('Hostel', 'Hostel'),
        ('Bus', 'Bus'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_CHOICES)
    description = models.TextField()

    summary = models.TextField(blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.student_name} - {self.complaint_type}"



class Resource(models.Model):

    CATEGORY_CHOICES = [
        ('PPT', 'PPT'),
        ('Question Paper', 'Question Paper'),
        ('Notes', 'Notes'),
    ]

    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    # file = models.FileField(upload_to='resources/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.category}"


# ============================
# Discussion Models
# ============================

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.post.title}"


