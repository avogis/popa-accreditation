from django.core.exceptions import ValidationError
from django.test import TestCase
from mock import Mock, patch

from accreditation_app.models import AccreditatonApplication


class AccreditatonApplicationModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        firat_application = AccreditatonApplication()
        firat_application.first_name = 'Emily'
        firat_application.last_name = 'Svensson'
        firat_application.email = 'emily.svensson@test.com'
        firat_application.save()

        second_application = AccreditatonApplication()
        second_application.first_name = 'Jorge'
        second_application.last_name = 'Vargas'
        second_application.email = 'jorge.vargas@test.com'
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
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_surname(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = ''
        application.email = 'emily.vargas@test.com'
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    def test_cannot_save_empty_applications_email(self):
        application = AccreditatonApplication()
        application.first_name = 'Emily'
        application.last_name = 'Vargas'
        application.email = ''
        with self.assertRaises(ValidationError):
            application.save()
            application.full_clean()

    @patch('accreditation_app.models.PMMail', return_value=Mock())
    def test_when_reviewed_email_is_sent(self, mock_pm):
        mock_pm.send().return_value = 'OK'

        first_name = 'Emily',
        last_name = 'Vargas',
        email = 'emily.vargas@test.com'

        application = AccreditatonApplication.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        application.save()
        application = AccreditatonApplication.objects.get(pk=1)
        application.reviewed = True
        data = {
            'first_name': "{}".format(first_name),
            'last_name': "{}".format(last_name),
            'email': "{}".format(email),
        }
        application.save()
        mock_pm.assert_called_with(
            sender='elizaveta@popaganda.se',
            template_id=5293163,
            template_model=data,
            to='emily.vargas@test.com'
        )
