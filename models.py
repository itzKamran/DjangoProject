from django.db import models

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

    def __str__(self):
        return self.username


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    employer = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='jobs')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Full-time')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.job_title}"


class ChatMessage(models.Model):
    application = models.ForeignKey(
        JobApplication, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )
    sender = models.ForeignKey(
        UserInfo, 
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Msg from {self.sender.username} at {self.timestamp.strftime('%H:%M')}"


class Company(models.Model):
    employer = models.OneToOneField(
        UserInfo,
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.company_name


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('STATUS', 'Status Update'),
        ('CHAT', 'New Message'),
    )

    recipient = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    sender = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:20]}"
