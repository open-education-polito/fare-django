from django.urls import path

from fare.filesupload.views import (
    files_upload_view,
)

app_name = "filesupload"
urlpatterns = [
    path("upload", view=files_upload_view, name="files_upload"),
]
