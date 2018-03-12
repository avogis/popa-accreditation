from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from postmark.core import PMMail, PMMailSendException

from accreditation.settings import (
    POSTMARK_APPLICATION_SENT_TEMPLATE,
    POSTMARK_SENDER,
)


class AccreditatonApplication(models.Model):
    first_name = models.CharField(null=False, blank=False, max_length=50, default='')
    last_name = models.CharField(null=False, blank=False, max_length=50, default='')
    email = models.EmailField(null=False, blank=False, default='')
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.email)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.reviewed:
            data = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
            }
            try:
                pm = PMMail(
                    to=self.email,
                    sender=POSTMARK_SENDER,
                    template_id=POSTMARK_APPLICATION_SENT_TEMPLATE,
                    template_model=data
                )
                pm.send()
                super(AccreditatonApplication, self).save(*args, **kwargs)
            except PMMailSendException:
                raise Exception
        else:
            super(AccreditatonApplication, self).save(*args, **kwargs)
