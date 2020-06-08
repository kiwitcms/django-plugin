from unittest import skip, expectedFailure
from django.test import SimpleTestCase
from django.urls import reverse


class TestAppContactPageTest(SimpleTestCase):
    def test_contact_page(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        raise Exception


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


class TestAppBooleanPageTest(SimpleTestCase):
    def test_get_correct_boolean(self):
        with self.subTest("Should return False"):
            false_response = self.client.get('/testapp/boolean/0/')
            self.assertEqual(false_response.content, b'False')
        with self.subTest("Should return True"):
            true_response = self.client.get('/testapp/boolean/1/')
            self.assertEqual(true_response.content, b'True')
        with self.subTest("Should return invalid"):
            invalid_response = self.client.get('/testapp/boolean/99/')
            self.assertEqual(invalid_response.content, b'invalid')
