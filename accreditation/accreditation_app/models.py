from django.db import models


# Create your models here.
class AccreditatonApplication(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=50, default='')
    last_name = models.CharField(null=False, blank=False, max_length=50, default='')
    email = models.EmailField(null=False, blank=False, default='')
