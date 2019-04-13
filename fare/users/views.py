from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import HttpResponseRedirect

User = get_user_model()


class ChangeStaffPermissionView(LoginRequiredMixin, UpdateView):
    """
    This class allows to change the staff_member permission of a user

    :attr http_methods_names: allowed http methods for this class
    :type http_methods_names: list
    :attr model: reference model used by this class
    :type model: User
    :attr slug_field: store and generate a valid url form the username of the requested user
    :type slug_field: string
    :attr slug_url_kwarg: tell the view to get the url kwarg named as specified in slug_field
    :type slug_url_kwarg: dictionary
    :attr fields: fields that can be modified
    :type fields: set
    :attr template_name_suffix: suffix that indicates the right template
    :type template_name_suffix: string

    """
    http_method_names = ['post', 'get']
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    fields = ('staff_member',)
    template_name_suffix = '_change_permission'

    def get(self, request, *args, **kwargs):
        """
        Manage the GET request, if the user has the permission and the requested user is not an admin,
        display the page where the he can modify the requested user's permission 
        """
        # verify if the user is a staff member and the requested user is not an admin
        if request.user.staff_member and not User.objects.get(username=kwargs['username']).is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def post(self, request, *args, **kwargs):
        """
        Manage the POST request, check the permission and if the user has it, 
        change the field of the requested user unless he is an admin
        """
        # verify if the user is a staff member and the requested user is not an admin
        if request.user.staff_member and not User.objects.get(username=kwargs['username']).is_superuser:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_success_url(self):
        """
        url where the user is redirected after a successful operation
        """
        return reverse("users:list")


change_permission_view = ChangeStaffPermissionView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
