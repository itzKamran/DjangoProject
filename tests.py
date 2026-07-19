from django.test import TestCase
from django.urls import reverse

from .models import UserInfo


class UserRegistrationTests(TestCase):
    def test_user_can_register_and_be_saved(self):
        response = self.client.post(
            reverse('create-user'),
            {
                'name': 'John Doe',
                'email': 'john@example.com',
                'mobile_no': '9876543210',
                'uname': 'johndoe',
                'passwd': 'secret123',
                'confirm_passwd': 'secret123',
                'role': 'Job Seeker',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserInfo.objects.filter(username='johndoe').exists())
        saved_user = UserInfo.objects.get(username='johndoe')
        self.assertEqual(saved_user.full_name, 'John Doe')
        self.assertEqual(saved_user.email, 'john@example.com')

    def test_user_can_login_and_reach_home_page(self):
        UserInfo.objects.create(
            full_name='Jane Doe',
            email='jane@example.com',
            mobile_no='9876543211',
            username='janedoe',
            password='secret123',
            role='Job Seeker',
        )

        response = self.client.post(
            reverse('login-user'),
            {
                'uname': 'janedoe',
                'passwd': 'secret123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('jobseeker-page'))

    def test_employer_user_redirects_to_employer_page(self):
        UserInfo.objects.create(
            full_name='Mark Doe',
            email='mark@example.com',
            mobile_no='9876543212',
            username='markdoe',
            password='secret123',
            role='Employer',
        )

        response = self.client.post(
            reverse('login-user'),
            {
                'uname': 'markdoe',
                'passwd': 'secret123',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('employer-page'))

    def test_profile_update_saves_new_details(self):
        user = UserInfo.objects.create(
            full_name='Sara Doe',
            email='sara@example.com',
            mobile_no='9876543213',
            username='saradoe',
            password='secret123',
            role='Job Seeker',
        )
        session = self.client.session
        session['logged_in_user'] = user.username
        session.save()

        response = self.client.post(
            reverse('update-profile'),
            {
                'name': 'Sara Updated',
                'email': 'sara.updated@example.com',
                'mobile_no': '9999999999',
            },
        )

        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.full_name, 'Sara Updated')
        self.assertEqual(user.email, 'sara.updated@example.com')
        self.assertEqual(user.mobile_no, 9999999999)
