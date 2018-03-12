from django.test import TestCase


class AccreditationPageTest(TestCase):

    def test_uses_accreditation_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'accreditation.html')

    def test_accreditation_page_returns_correct_html(self):
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Popaganda Accreditation</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'accreditation.html')


class UserApplicationAcceptedPageTest(TestCase):

    def test_uses_application_accepted(self):
        response = self.client.get('/accreditation_app/application_accepted/')
        self.assertTemplateUsed(response, 'application_accepted.html')
