from django.db import models

# Create your models here.

class NmapScan(models.model):
    target_ip = models.CharField(max_length=100)
    scan_date = models.DateTimeField(auto_now_add=True)
    results = models.TextField()  
