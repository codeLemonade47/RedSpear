from django.db import models

# Create your models here.
# scanner/models.py

class ScanResult(models.Model):
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)


class WebsiteScan(models.Model):
    website_url = models.URLField(max_length=200)
    scan_start_time = models.DateTimeField(auto_now_add=True)
    scan_end_time = models.DateTimeField(null=True, blank=True)
    results = models.TextField()  # For storing the scan results