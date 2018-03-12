from django.core.exceptions import ValidationError
from django.test import TestCase

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
