from django.db import models

# Create your models here.
ROLE_CHOICES = [
    ("Job Seeker", "Job Seeker"),
    ("Employer", "Employer"),
]

class UserInfo(models.Model):
    full_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    mobile_no = models.BigIntegerField(null=True, blank=True)
    username = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = "userinfo"