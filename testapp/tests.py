from django.test import SimpleTestCase
from django.urls import reverse
from unittest import skip, expectedFailure


class TestAppContactPageTest(SimpleTestCase):
    def test_contact_page(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppAboutPageTest(SimpleTestCase):
    def test_about_page(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppIndexPageTest(SimpleTestCase):
    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't have run")


class TestAppMissingPageTest(SimpleTestCase):
    def test_missing_page(self):
        response = self.client.get('/testapp/missing')
        self.assertEqual(response.status_code, 200)

    @expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")

    @expectedFailure
    def test_unexpected_success(self):
        self.assertEqual(1, 1, "broken (not actually)")
