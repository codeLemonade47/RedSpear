from django.db import models

# Create your models here.

class Report(models.Model):
    ip = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    report_file = models.FileField(upload_to="reports/%Y/%m/%d")
    report_date = models.DateTimeField(auto_now_add=True)  
