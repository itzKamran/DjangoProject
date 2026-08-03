from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    ChatMessage,
    Company,
    Job,
    JobApplication,
    Notification,
    UserInfo,
)

# ==========================================
# Session Authentication Helpers
# ==========================================

def get_logged_in_user(request):
    """Retrieves active user from session."""
    username = request.session.get('logged_in_user')
    if not username:
        return None
    return UserInfo.objects.filter(username=username).first()


def CreateUserPage(request):
    return render(request, 'index.html')


def CreateUser(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        mobile_number = request.POST.get('mobile_no', '')
        username = request.POST.get('uname', '')
        password = request.POST.get('passwd', '')
        confirm_passwd = request.POST.get('confirm_passwd', '')
        role = request.POST.get('role', '')

        if not username or not password:
            return render(request, 'index.html', {'message': 'Username and password are required!'})

        if password != confirm_passwd:
            return render(request, 'index.html', {'message': 'Password does not match!'})

        if UserInfo.objects.filter(username=username).exists():
            return render(request, 'index.html', {'message': 'Username already exists!'})

        UserInfo.objects.create(
            full_name=name,
            email=email,
            mobile_no=mobile_number,
            username=username,
            password=password,
            role=role,
        )
        return redirect('login-page')

    return render(request, 'index.html')


def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('uname', '')
        password = request.POST.get('passwd', '')

        user = UserInfo.objects.filter(username=username, password=password).first()
        if user is not None:
            request.session['logged_in_user'] = user.username
            if user.role == 'Employer':
                return redirect('employer-page')
            return redirect('jobseeker-page')

        return render(request, 'login.html', {'message': 'Invalid username or password!'})

    return render(request, 'login.html')


def EmployerPage(request):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')
    return render(request, 'employer.html', {'user': user})


def JobSeekerPage(request):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')
    return render(request, 'jobseeker.html', {'user': user})


def UpdateProfile(request):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')

    if request.method == 'POST':
        user.full_name = request.POST.get('name', user.full_name)
        user.email = request.POST.get('email', user.email)
        user.mobile_no = request.POST.get('mobile_no', user.mobile_no)
        user.password = request.POST.get('password', user.password)
        user.save()

    if user.role == 'Employer':
        return redirect('employer-page')
    return redirect('jobseeker-page')


def LogoutUser(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
    return redirect('login-page')


# ==========================================
# Job Management
# ==========================================

def add_job(request):
    employer = get_logged_in_user(request)
    if employer is None:
        return redirect('login-page')

    if request.method == "POST":
        Job.objects.create(
            employer=employer,
            job_title=request.POST.get("job_title"),
            company_name=request.POST.get("company_name"),
            location=request.POST.get("location"),
            salary=request.POST.get("salary"),
            job_type=request.POST.get("job_type"),
            description=request.POST.get("description")
        )
        return redirect("my_jobs")

    return render(request, "add_job.html", {"user": employer})


def my_jobs(request):
    employer = get_logged_in_user(request)
    if employer is None:
        return redirect('login-page')

    jobs = Job.objects.filter(employer=employer).order_by("-created_at")
    return render(request, "my_jobs.html", {"user": employer, "jobs": jobs})


def edit_job(request, id):
    employer = get_logged_in_user(request)
    if employer is None:
        return redirect('login-page')

    job = Job.objects.filter(id=id, employer=employer).first()
    if not job:
        return redirect("my_jobs")

    if request.method == "POST":
        job.job_title = request.POST.get("job_title")
        job.company_name = request.POST.get("company_name")
        job.location = request.POST.get("location")
        job.salary = request.POST.get("salary")
        job.job_type = request.POST.get("job_type")
        job.description = request.POST.get("description")
        job.save()
        return redirect("my_jobs")

    return render(request, "edit_job.html", {"job": job, "user": employer})


def delete_job(request, id):
    employer = get_logged_in_user(request)
    if employer is None:
        return redirect('login-page')

    job = Job.objects.filter(id=id, employer=employer).first()
    if job:
        job.delete()

    return redirect("my_jobs")


# ==========================================
# Applications & Job Search
# ==========================================

def view_jobs(request):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')

    query = request.GET.get('q', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    location = request.GET.get('location', '').strip()

    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(job_title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(description__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'view_jobs.html', {
        'user': user,
        'jobs': jobs,
        'query': query,
        'selected_job_type': job_type,
        'selected_location': location,
    })


def job_detail(request, id):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')

    job = get_object_or_404(Job, id=id)

    has_applied = False
    if user.role == 'Job Seeker':
        has_applied = JobApplication.objects.filter(job=job, applicant=user).exists()

    if request.method == 'POST':
        if user.role != 'Job Seeker':
            return render(request, 'job_detail.html', {
                'job': job,
                'user': user,
                'error': 'Only job seekers can apply for jobs.'
            })

        if has_applied:
            return render(request, 'job_detail.html', {
                'job': job,
                'user': user,
                'has_applied': True,
                'error': 'You have already applied for this job.'
            })

        # Resume is now optional (will accept files if sent, or proceed without error)
        resume_file = request.FILES.get('resume', None)

        JobApplication.objects.create(
            job=job,
            applicant=user,
            resume=resume_file,
            status='Pending'
        )

        return redirect('my-applications')

    return render(request, 'job_detail.html', {
        'job': job,
        'user': user,
        'has_applied': has_applied,
    })


def my_applications(request):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')

    applications = JobApplication.objects.filter(applicant=user).select_related('job').order_by('-applied_at')
    return render(request, 'my_applications.html', {'applications': applications})


def employer_applications(request):
    user = get_logged_in_user(request)
    if user is None or user.role != 'Employer':
        return redirect('login-page')

    applications = JobApplication.objects.filter(job__employer=user).select_related('job', 'applicant')
    return render(request, 'employer_applications.html', {'applications': applications})


def update_application_status(request, app_id, status):
    user = get_logged_in_user(request)
    if user is None or user.role != 'Employer':
        return redirect('login-page')

    application = get_object_or_404(JobApplication, id=app_id, job__employer=user)
    if status in ['Accepted', 'Rejected']:
        application.status = status
        application.save()

    return redirect('employer-applications')


# ==========================================
# Company Profiles
# ==========================================

def manage_company(request):
    employer = get_logged_in_user(request)
    if employer is None or employer.role != 'Employer':
        return redirect('login-page')

    company = Company.objects.filter(employer=employer).first()

    if request.method == "POST":
        company_name = request.POST.get("company_name")
        address = request.POST.get("address")
        website = request.POST.get("website")
        description = request.POST.get("description")

        if company:
            company.company_name = company_name
            company.address = address
            company.website = website
            company.description = description
            company.save()
        else:
            Company.objects.create(
                employer=employer,
                company_name=company_name,
                address=address,
                website=website,
                description=description
            )
        return redirect('employer-page')

    if company:
        return render(request, "edit_company.html", {"user": employer, "company": company})

    return render(request, "create_company.html", {"user": employer})


def company_detail(request, company_id):
    user = get_logged_in_user(request)
    if user is None:
        return redirect('login-page')

    company = get_object_or_404(Company, id=company_id)
    company_jobs = Job.objects.filter(employer=company.employer).order_by('-created_at')

    return render(request, "company_detail.html", {
        "user": user,
        "company": company,
        "jobs": company_jobs
    })


# ==========================================
# Chat & Real-Time Messaging Fixes
# ==========================================

def application_chat(request, application_id):
    user = get_logged_in_user(request)
    if not user:
        return redirect('login-page')

    application = get_object_or_404(JobApplication, id=application_id)

    # Security check: Only applicant or job employer can view this chat
    if user != application.applicant and user != application.job.employer:
        return redirect('login-page')

    if request.method == "POST":
        msg_text = request.POST.get("message", "").strip()
        if msg_text:
            ChatMessage.objects.create(
                application=application,
                sender=user,
                message=msg_text
            )
        return redirect('application-chat', application_id=application_id)

    chat_messages = ChatMessage.objects.filter(application=application).order_by('timestamp')

    return render(request, "chat.html", {
        "user": user,
        "application": application,
        "messages": chat_messages
    })


def fetch_messages_api(request, application_id):
    user = get_logged_in_user(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    application = get_object_or_404(JobApplication, id=application_id)

    if user != application.applicant and user != application.job.employer:
        return JsonResponse({"error": "Forbidden"}, status=403)

    messages = ChatMessage.objects.filter(application=application).select_related('sender').order_by('timestamp')

    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "sender_name": msg.sender.full_name or msg.sender.username,
            "is_self": msg.sender.username == user.username,
            "message": msg.message,
            "time": msg.timestamp.strftime("%I:%M %p | %b %d")
        })

    return JsonResponse({"messages": formatted_messages})


# ==========================================
# Notifications
# ==========================================

def notifications_page(request):
    user = get_logged_in_user(request)
    if not user:
        return redirect('login-page')

    user_notifications = Notification.objects.filter(recipient=user)
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, "notifications.html", {
        "user": user,
        "notifications": user_notifications
    })


def unread_notifications_api(request):
    user = get_logged_in_user(request)
    if not user:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    unread_notifications = Notification.objects.filter(recipient=user, is_read=False)

    preview = []
    for notif in unread_notifications[:5]:
        preview.append({
            "id": notif.id,
            "type": notif.notification_type,
            "message": notif.message,
            "link": notif.link or "#",
            "time": notif.created_at.strftime("%b %d, %I:%M %p")
        })

    return JsonResponse({
        "unread_count": unread_notifications.count(),
        "notifications": preview
    })
