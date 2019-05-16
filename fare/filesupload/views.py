from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import DocumentForm
from django.views.generic.edit import FormView


class FileFieldView(FormView):
    form_class = DocumentForm
    template_name = 'filesupload.html'
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
