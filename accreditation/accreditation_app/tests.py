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

    def test_accreditation_page_returns_correct_html(self):
        first_name = 'Emily'
        last_name = 'Svensson'
        email = 'emily.svensson@test.com'
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }
        response = self.client.post(
            '/',
            data
        )
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Application Accepted</title>', html)
        self.assertIn('<h1>Your application has been accepted</h1>', html)
        self.assertIn(
            '<p>{} {} an email with further information was sent to {}</p>'.format(
                first_name,
                last_name,
                email
            ),
            html
        )
        self.assertTrue(html.strip().endswith('</html>'))

        self.assertTemplateUsed(response, 'application_accepted.html')
