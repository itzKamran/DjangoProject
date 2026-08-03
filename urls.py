from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.CreateUserPage, name='create-page'),
    path('create-user/', views.CreateUser, name='create-user'),
    path('login-page/', views.LoginUser, name='login-page'),
    path('login-user/', views.LoginUser, name='login-user'),
    path('logout/', views.LogoutUser, name='logout'),
    
    # User Dashboards & Profile
    path('employer/', views.EmployerPage, name='employer-page'),
    path('jobseeker/', views.JobSeekerPage, name='jobseeker-page'),
    path('update-profile/', views.UpdateProfile, name='update-profile'),
    
    # Employer Job Actions
    path("add-job/", views.add_job, name="add_job"),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("edit-job/<int:id>/", views.edit_job, name="edit_job"),
    path("delete-job/<int:id>/", views.delete_job, name="delete_job"),
    path("employer/applications/", views.employer_applications, name="employer-applications"),
    path("application/<int:app_id>/status/<str:status>/", views.update_application_status, name="update-app-status"),
    
    # Job Seeker Actions
    path("jobs/", views.view_jobs, name="view-jobs"),
    path("jobs/<int:id>/", views.job_detail, name="job-detail"),
    path("my-applications/", views.my_applications, name="my-applications"),
    
    # Company Profile
    path("company/manage/", views.manage_company, name="manage-company"),
    path("company/<int:company_id>/", views.company_detail, name="company-detail"),
    
    # Chat & Real-Time APIs
    path("chat/<int:application_id>/", views.application_chat, name="application-chat"),
    path("api/chat/<int:application_id>/fetch/", views.fetch_messages_api, name="fetch-messages-api"),
    
    # Notifications
    path("notifications/", views.notifications_page, name="notifications-page"),
    path("api/notifications/unread/", views.unread_notifications_api, name="unread-notifications-api"),
]
