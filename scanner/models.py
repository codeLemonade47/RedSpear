from django.db import models

# Create your models here.
# scanner/models.py

class ScanResult(models.Model):
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17)


