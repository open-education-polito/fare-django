from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    school_level = models.CharField(max_length=255)
    school_subject = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
