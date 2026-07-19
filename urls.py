from django.urls import path
from . import views

urlpatterns = [
    path('getcreatepage/', views.CreateUserPage, name='create-page'),
    path('create-user/', views.CreateUser, name='create-user'),
    path('login-page/', views.LoginUser, name='login-page'),
    path('login-user/', views.LoginUser, name='login-user'),
    path('employer/', views.EmployerPage, name='employer-page'),
    path('jobseeker/', views.JobSeekerPage, name='jobseeker-page'),
    path('update-profile/', views.UpdateProfile, name='update-profile'),
    path('logout/', views.LogoutUser, name='logout'),
]