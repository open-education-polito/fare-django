import pytest
from django.conf import settings
from django.test import RequestFactory, Client, TestCase
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from fare.users.views import UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db
MyUser = get_user_model()


class TestUserChangePermissions(TestCase):
    """
    TODO:
        test user's permission 'staff_member'
    """

    def test_user_get_permission_page(self):
        """
        A user without staff_member permission perform a GET on another user's permission
        page to change the staff_member permission and fail
        user (GET)--> user (permission page)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.get(reverse('users:staff_permission', kwargs={'username': username2}), follow=True)

        self.assertRedirects(response=response, expected_url='/', status_code=302, target_status_code=200)

    def test_user_post_permission(self):
        """
        A user without staff_member permission perform a POST to change another user's permission
        user (POST)--> user (permission)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.post(reverse('users:staff_permission', kwargs={'username': username2}), follow=True)

        self.assertRedirects(response=response, expected_url='/', status_code=302, target_status_code=200)

    def test_staff_get_permission_page(self):
        """
        A user with staff_member permission perform a GET to another user's permission page
        staff (GET)--> user (permission page)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.staff_member = True
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.get(reverse('users:staff_permission', kwargs={'username': username2}), follow=True)

        self.assertTemplateUsed(response, 'users/user_change_permission.html')
        self.assertEqual(response.status_code, 200)

    def test_staff_post_permission(self):
        """
        A user with staff_member permission perform a POST to change another user's permission
        staff (POST)--> user (permission)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'
        data = {'staff_member': 'on'}

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.staff_member = True
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.post(
                                reverse('users:staff_permission', kwargs={'username': username2}),
                                data,
                                follow=True
                            )

        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.get(username=username2).staff_member, True)

    def test_staff_post_staff_permission(self):
        """
        A user with staff_member permission perform a POST to change another staff's permission
        staff (POST)--> staff (permission)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.staff_member = True
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.staff_member = True
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.post(reverse('users:staff_permission', kwargs={'username': username2}), follow=True)

        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.get(username=username2).staff_member, False)

    def test_staff_get_admin_permission_page(self):
        """
        A user with staff_member permission perform a GET to an admin's permission page
        staff (GET)--> admin (permission page)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.staff_member = True
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.is_superuser = True
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.get(reverse('users:staff_permission', kwargs={'username': username2}))

        self.assertTemplateNotUsed(response, 'users/user_change_permission.html')
        self.assertEqual(response.status_code, 302)

    def test_staff_post_admin_permission(self):
        """
        A user with staff_member permission perform a POST to change admin's permission
        staff (POST)--> admin (permission)
        """
        username1 = 'TestUser1'
        email1 = 'testUser1@mail.com'
        password1 = 'test_password'
        username2 = 'TestUser2'
        email2 = 'testUser2@mail.com'
        password2 = 'test_password'

        user1 = MyUser.objects.create_user(username=username1, email=email1, password=password1)
        user1.staff_member = True
        user1.save()

        user2 = MyUser.objects.create_user(username=username2, email=email2, password=password2)
        user2.is_superuser = True
        user2.staff_member = True
        user2.save()

        client = Client()
        client.login(username=username1, password=password1)

        response = client.post(reverse('users:staff_permission', kwargs={'username': username2}), follow=True)

        self.assertTemplateNotUsed(response, 'users/user_change_permission.html')
        self.assertTemplateUsed(response, 'pages/home.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MyUser.objects.get(username=username2).staff_member, True)


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:

    def test_get_redirect_url(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"
