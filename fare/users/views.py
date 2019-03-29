from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import HttpResponseRedirect

User = get_user_model()


class ChangeStaffPermissionView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post', 'get']
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    fields = ('staff_member',)
    template_name_suffix = '_change_permission'

    def get(self, request, *args, **kwargs):
        if request.user.staff_member:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def post(self, request, *args, **kwargs):
        if request.user.staff_member:
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("home"))

    def get_success_url(self):
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
