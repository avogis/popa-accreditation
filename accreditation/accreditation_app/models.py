from django.core.exceptions import ValidationError
from django.db import models
from postmark.core import PMMail, PMMailSendException

from accreditation.settings import (
    ACCREDITATION_CHOICE_PHOTO,
    ACCREDITATION_CHOICE_JOURNALIST,
    ACCREDITATION_CHOICE_FESTIVAl,
    PHOTO_A,
    PHOTO_B,
    PHOTO_C,
    POSTMARK_APPLICATION_DECLINE_TEMPLATE,
    POSTMARK_APPLICATION_DISCOUNT_TEMPLATE,
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
        (ACCREDITATION_CHOICE_PHOTO, 'Photo Pass'),
        (ACCREDITATION_CHOICE_JOURNALIST, 'Journalist Pass'),
        (ACCREDITATION_CHOICE_FESTIVAl, 'Festival Pass'),
    )
    TYPE_OF_PHOTO_CHOICES = (
        (PHOTO_A, 'Photo Pass A'),
        (PHOTO_B, 'Photo Pass B'),
        (PHOTO_C, 'Photo Pass C'),
    )

    first_name = models.CharField(null=False, blank=False, max_length=50, default='')
    last_name = models.CharField(null=False, blank=False, max_length=50, default='')
    email = models.EmailField(null=False, blank=False, default='')
    granted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    application = models.TextField(null=False, blank=False, default=None)
    applied = models.DateTimeField(auto_now_add=True)
    discount_amount = models.IntegerField(null=True, blank=True, default=None)
    discount_code = models.CharField(null=True, blank=True, max_length=50, default=None)
    type_of_accreditation = models.CharField(
        null=False,
        blank=False,
        max_length=9,
        choices=TYPE_OF_ACCREDITATION_CHOICES,
        default=None,
    )
    photo_type = models.CharField(
        null=True,
        blank=True,
        max_length=1,
        choices=TYPE_OF_PHOTO_CHOICES,
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
            template_id = POSTMARK_APPLICATION_GRANT_TEMPLATE
            if self.discount_amount and self.discount_code:
                data['discount_amount'] = self.discount_amount
                data['discount_code'] = self.discount_code
                template_id = POSTMARK_APPLICATION_DISCOUNT_TEMPLATE
            try:
                send_email(
                    data,
                    template_id,
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
