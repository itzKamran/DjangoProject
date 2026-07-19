from django.shortcuts import redirect, render

from .models import UserInfo


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


def get_logged_in_user(request):
    username = request.session.get('logged_in_user')
    if not username:
        return None
    return UserInfo.objects.filter(username=username).first()


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
        user.save()

    if user.role == 'Employer':
        return redirect('employer-page')
    return redirect('jobseeker-page')


def LogoutUser(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
    return redirect('login-page')