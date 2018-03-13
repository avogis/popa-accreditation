from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import Mock, patch

from accreditation_app.models import AccreditatonApplication
from accreditation.settings import (
    POSTMARK_APPLICATION_DECLINE_TEMPLATE,
    POSTMARK_APPLICATION_GRANT_TEMPLATE,
    POSTMARK_SENDER,
)


class AccreditatonApplicationModelTest(TestCase):
    first_name = 'Emily',
    last_name = 'Vargas',
    email = 'emily.vargas@test.com'
    type_of_accreditation = 'photo'
    application_text = 'Photographer'

    @patch('accreditation_app.models.send_email', return_value=Mock())
    def test_saving_and_retrieving_items(self, mock_email):
        firat_application = AccreditatonApplication()
        firat_application.first_name = self.first_name
        firat_application.last_name = self.last_name
        firat_application.email = self.email
        firat_application.type_of_accreditation = self.type_of_accreditation
        firat_application.application = self.application_text
        firat_application.save()
        mock_email.assert_not_called()

        second_application = AccreditatonApplication()
        second_application.first_name = 'Jorge'
        second_application.last_name = self.last_name
        second_application.email = self.email
        second_application.type_of_accreditation = self.type_of_accreditation
        second_application.application = self.application_text
        second_application.save()
        mock_email.assert_not_called()

        saved_applications = AccreditatonApplication.objects.all()
        self.assertEqual(saved_applications.count(), 2)

        first_saved_item = saved_applications[0]
        second_saved_item = saved_applications[1]
        self.assertEqual(first_saved_item.first_name, "{}".format(self.first_name))
        self.assertEqual(second_saved_item.first_name, 'Jorge')

    def test_cannot_save_empty_applications_name(self):
        application = AccreditatonApplication()
        application.first_name = ''
        application.last_name = self.last_name
        application.email = self.email
        application.type_of_accreditation = self.type_of_accreditation
        application.application = self.application_text
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_surname(self):
        application = AccreditatonApplication()
        application.first_name = self.first_name
        application.last_name = ''
        application.email = self.email
        application.type_of_accreditation = self.type_of_accreditation
        application.application = self.application_text
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_email(self):
        application = AccreditatonApplication()
        application.first_name = self.first_name
        application.last_name = self.last_name
        application.email = ''
        application.type_of_accreditation = self.type_of_accreditation
        application.application = self.application_text
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_application(self):
        application = AccreditatonApplication()
        application.first_name = self.first_name
        application.last_name = self.last_name
        application.email = self.email
        application.type_of_accreditation = self.type_of_accreditation
        application.application = ''
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_type_of_accriditation_application(self):
        application = AccreditatonApplication()
        application.first_name = self.first_name
        application.last_name = self.last_name
        application.email = self.email
        application.type_of_accreditation = ''
        application.application = self.application_text
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()


@patch('accreditation_app.models.send_email', return_value=Mock())
class AccreditatonApplicationModelTestSendsEmail(TestCase):
    first_name = 'Emily',
    last_name = 'Vargas',
    email = 'emily.vargas@test.com'
    type_of_accreditation = 'photo'
    application_text = 'Photographer'

    data = {
        'first_name': "{}".format(first_name),
        'last_name': "{}".format(last_name),
        'email': "{}".format(email),
    }

    def test_when_granted_email_is_sent(self, mock_email):
        application = AccreditatonApplication.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            type_of_accreditation=self.type_of_accreditation,
            application=self.application_text
        )

        mock_email.assert_not_called()

        application = AccreditatonApplication.objects.get(pk=1)
        application.granted = True
        application.declined = False
        application.save()

        mock_email.assert_called_once_with(
            self.data,
            POSTMARK_APPLICATION_GRANT_TEMPLATE,
            POSTMARK_SENDER,
        )

    def test_when_declined_email_is_sent(self, mock_email):
        application = AccreditatonApplication.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            type_of_accreditation=self.type_of_accreditation,
            application=self.application_text
        )

        mock_email.assert_not_called()

        application = AccreditatonApplication.objects.get(pk=1)
        application.granted = False
        application.declined = True
        application.save()

        mock_email.assert_called_with(
            self.data,
            POSTMARK_APPLICATION_DECLINE_TEMPLATE,
            POSTMARK_SENDER,
        )


class AccreditatonApplicationModelRaisesErrorWhenIncorrectData(TestCase):
    first_name = 'Emily',
    last_name = 'Vargas',
    email = 'emily.vargas@test.com'
    type_of_accreditation = 'photo'
    application_text = 'Photographer'

    def test_cannot_save_both_declined_and_granted_application(self):
        application = AccreditatonApplication()
        application.first_name = self.first_name
        application.last_name = self.last_name
        application.email = self.email
        application.type_of_accreditation = self.type_of_accreditation
        application.application = self.application_text
        application.granted = True
        application.declined = True
        with self.assertRaises(ValidationError):
            application.save()
