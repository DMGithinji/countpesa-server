from django.db import models

class UploadedFile(models.Model):
    content = models.TextField()
