from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from accreditation_app.views import accreditation_page


class AccreditationPageTest(TestCase):

    def test_root_url_resolves_to_accreditation_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, accreditation_page)

    def test_accreditation_page_returns_correct_html(self):
        request = HttpRequest()
        response = accreditation_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Popaganda Accreditation</title>', html)
        self.assertTrue(html.endswith('</html>'))
