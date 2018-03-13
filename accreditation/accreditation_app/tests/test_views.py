from django.test import TestCase
from mock import Mock, patch

from accreditation_app.models import AccreditatonApplication


def assert_data(test, data):
    response = test.client.post('/', data)
    test.assertEqual(response.status_code, 200)
    test.assertTemplateUsed(response, 'application_accepted.html')
    expected_error = (
        "This field cannot be blank"
    )
    html = response.content.decode('utf8')
    test.assertIn(expected_error, html)


class AccreditationPageTest(TestCase):

    def test_uses_accreditation_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accreditation.html')

    def test_accreditation_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Popaganda Accreditation</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'accreditation.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(AccreditatonApplication.objects.count(), 0)


class UserApplicationAcceptedPageTest(TestCase):

    first_name = 'Emily'
    last_name = 'Svensson'
    email = 'emily.svensson@test.com'
    type_of_accreditation = 'photo'
    application = 'I am photographer'

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'type_of_accreditation': type_of_accreditation,
        'application': application
    }

    @patch('accreditation_app.views.PMMail', return_value=Mock())
    def test_accreditation_page_returns_correct_html(self, pm_mock):
        pm_mock.send().return_value = 'OK'
        response = self.client.post('/', self.data)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Application Accepted</title>', html)
        self.assertIn('<h1>Your application has been accepted</h1>', html)
        self.assertIn(
            '{} {} an email with further information was sent to {}'.format(
                self.first_name,
                self.last_name,
                self.email
            ),
            html
        )
        self.assertIn(self.application, html)
        self.assertIn(self.type_of_accreditation, html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'application_accepted.html')

    @patch('accreditation_app.views.PMMail', return_value=Mock())
    def test_can_save_a_POST_request(self, pm_mock):
        response = self.client.post('/', self.data)
        pm_mock.send().return_value = 'OK'
        self.assertEqual(AccreditatonApplication.objects.count(), 1)
        new_application = AccreditatonApplication.objects.first()
        self.assertEqual(new_application.first_name, self.first_name)

        self.assertIn('Your application has been accepted', response.content.decode())
        self.assertTemplateUsed(response, 'application_accepted.html')

    def test_validation_error_name_is_sent_back_to_application_accepted_template(self):
        data = {
            'first_name': '',
            'last_name': self.last_name,
            'email': self.email,
            'type_of_accreditation': self.type_of_accreditation,
            'application': self.application
        }
        assert_data(self, data)

    def test_validation_error_surname_is_sent_back_to_application_accepted_template(self):
        data = {
            'first_name': self.first_name,
            'last_name': '',
            'email': self.email,
            'type_of_accreditation': self.type_of_accreditation,
            'application': self.application
        }
        assert_data(self, data)

    def test_validation_error_email_is_sent_back_to_application_accepted_template(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': '',
            'type_of_accreditation': self.type_of_accreditation,
            'application': self.application
        }
        assert_data(self, data)

    def test_validation_error_application_is_sent_back_to_application_accepted_template(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'type_of_accreditation': self.type_of_accreditation,
            'application': ''
        }
        assert_data(self, data)

    def test_validation_error_type_of_accreditation_is_sent_back_to_application_accepted_template(
        self
    ):
        data = {
            'first_name': 'Emily',
            'last_name': 'Svensson',
            'email': self.email,
            'type_of_accreditation': '',
            'application': self.application
        }
        assert_data(self, data)

    def test_invalid_list_items_arent_saved(self):
        data = {
            'first_name': 'Emily',
            'last_name': 'Svensson',
            'email': '',
            'type_of_accreditation': self.type_of_accreditation,
            'application': self.application
        }
        self.client.post('/', data)
        self.assertEqual(AccreditatonApplication.objects.count(), 0)
