from django.db import models

class UploadedFile(models.Model):
    content = models.TextField()  # New field to store PDF text content
