from django.core.exceptions import ValidationError
from django.db import models
from postmark.core import PMMail, PMMailSendException

from accreditation.settings import (
    POSTMARK_APPLICATION_DECLINE_TEMPLATE,
    POSTMARK_APPLICATION_GRANT_TEMPLATE,
    POSTMARK_SENDER,
)


def send_email(data, template_id=POSTMARK_APPLICATION_DECLINE_TEMPLATE, sender=POSTMARK_SENDER):
    pm = PMMail(
        to=data['email'],
        sender=POSTMARK_SENDER,
        template_id=POSTMARK_APPLICATION_GRANT_TEMPLATE,
        template_model=data
    )
    pm.send()


class AccreditatonApplication(models.Model):
    TYPE_OF_ACCREDITATION_CHOICES = (
        ('photo', 'Photo Pass'),
        ('jounalist', 'Journalist Pass'),
        ('festival', 'Festival Pass'),
    )

    first_name = models.CharField(null=False, blank=False, max_length=50, default='')
    last_name = models.CharField(null=False, blank=False, max_length=50, default='')
    email = models.EmailField(null=False, blank=False, default='')
    granted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    application = models.TextField(null=False, blank=False, default=None)
    applied = models.DateTimeField(auto_now_add=True)
    type_of_accreditation = models.CharField(
        null=False,
        blank=False,
        max_length=9,
        choices=TYPE_OF_ACCREDITATION_CHOICES,
        default=None,
    )

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.email)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
        if self.granted and self.declined:
            raise ValidationError("Granted and declined are mutually exclusive.")
        if self.granted:
            try:
                send_email(
                    data,
                    POSTMARK_APPLICATION_GRANT_TEMPLATE,
                    POSTMARK_SENDER,
                )
                super(AccreditatonApplication, self).save(*args, **kwargs)
            except PMMailSendException:
                raise Exception
        elif self.declined:
            try:
                send_email(
                    data,
                    POSTMARK_APPLICATION_DECLINE_TEMPLATE,
                    POSTMARK_SENDER,
                )
                super(AccreditatonApplication, self).save(*args, **kwargs)
            except PMMailSendException:
                raise Exception
        else:
            super(AccreditatonApplication, self).save(*args, **kwargs)
