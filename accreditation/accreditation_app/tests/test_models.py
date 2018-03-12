from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import Mock, patch

from accreditation_app.models import AccreditatonApplication
from accreditation.settings import (
    POSTMARK_APPLICATION_GRANTE_TEMPLATE,
    POSTMARK_SENDER,
)


class AccreditatonApplicationModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        firat_application = AccreditatonApplication()
        firat_application.first_name = 'Emily'
        firat_application.last_name = 'Svensson'
        firat_application.email = 'emily.svensson@test.com'
        firat_application.type_of_accreditation = 'photo'
        firat_application.application = 'Photographer'
        firat_application.save()

        second_application = AccreditatonApplication()
        second_application.first_name = 'Jorge'
        second_application.last_name = 'Vargas'
        second_application.email = 'jorge.vargas@test.com'
        second_application.type_of_accreditation = 'photo'
        second_application.application = 'Photographer'
        second_application.save()

        saved_applications = AccreditatonApplication.objects.all()
        self.assertEqual(saved_applications.count(), 2)

        first_saved_item = saved_applications[0]
        second_saved_item = saved_applications[1]
        self.assertEqual(first_saved_item.first_name, 'Emily')
        self.assertEqual(second_saved_item.first_name, 'Jorge')

    def test_cannot_save_empty_applications_name(self):
        application = AccreditatonApplication()
        application.first_name = ''
        application.last_name = 'Vargas'
        application.email = 'jorge.vargas@test.com'
        application.type_of_accreditation = 'photo'
        application.application = 'Photographer'
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_surname(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = ''
        application.type_of_accreditation = 'photo'
        application.email = 'emily.vargas@test.com'
        application.application = 'Photographer'
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_email(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = 'Vargas'
        application.email = ''
        application.type_of_accreditation = 'photo'
        application.application = 'Photographer'
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_application(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = 'Vargas'
        application.email = 'emily.vargas@test.com'
        application.type_of_accreditation = 'photo'
        application.application = ''
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_type_of_accriditation_application(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = 'Vargas'
        application.email = 'emily.vargas@test.com'
        application.type_of_accreditation = ''
        application.application = 'Photographer'
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    @patch('accreditation_app.models.PMMail', return_value=Mock())
    def test_when_granted_email_is_sent(self, mock_pm):
        mock_pm.send().return_value = 'OK'

        first_name = 'Emily',
        last_name = 'Vargas',
        email = 'emily.vargas@test.com'
        type_of_accreditation = 'photo'
        application = 'Photographer'

        application = AccreditatonApplication.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            type_of_accreditation=type_of_accreditation,
            application=application
        )
        application.save()
        application = AccreditatonApplication.objects.get(pk=1)
        application.granted = True
        data = {
            'first_name': "{}".format(first_name),
            'last_name': "{}".format(last_name),
            'email': "{}".format(email),
        }
        application.save()
        mock_pm.assert_called_with(
            sender=POSTMARK_SENDER,
            template_id=POSTMARK_APPLICATION_GRANTE_TEMPLATE,
            template_model=data,
            to='emily.vargas@test.com'
        )
