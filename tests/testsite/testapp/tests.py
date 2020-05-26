from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class TestAppContactPageTest(TestCase):
    def test_contact_page(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppAboutPageTest(TestCase):
    def test_about_page(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppIndexPageTest(TestCase):
    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppMissingPageTest(TestCase):
    def test_missing_page(self):
        response = self.client.get('/testapp/missing')
        self.assertEqual(response.status_code, 404)
