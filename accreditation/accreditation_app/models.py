from django.db import models


class AccreditatonApplication(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=50, default='')
    last_name = models.CharField(null=False, blank=False, max_length=50, default='')
    email = models.EmailField(null=False, blank=False, default='')

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.email)
