from unittest import skip, expectedFailure
from django.test import TestCase
from django.urls import reverse
from .models import PageInfo


class TestAppContactPageTest(TestCase):
    def test_that_will_report_passed(self):
        PageInfo.objects.filter(page_title="pass").count()
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestAppAboutPageTest(TestCase):
    # pylint: disable=unreachable
    def test_that_will_report_error(self):
        PageInfo.objects.filter(page_title="error").count()
        url = reverse('about')
        response = self.client.get(url)
        raise Exception
        self.assertEqual(response.status_code, 200)


class TestAppIndexPageTest(TestCase):
    def test_index_page(self):
        PageInfo.objects.filter(page_title="pass").count()
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @skip("demonstrating skipping")
    def test_that_will_report_waived(self):
        self.fail("shouldn't have run")


class TestAppMissingPageTest(TestCase):
    def test_that_will_report_failed(self):
        PageInfo.objects.filter(page_title="fail").count()
        response = self.client.get('/testapp/missing')
        self.assertEqual(response.status_code, 200)

    @expectedFailure
    def test_expected_failure_reported_as_passed(self):
        self.assertEqual(1, 0, "broken")

    @expectedFailure
    def test_unexpected_success_reported_as_failed(self):
        self.assertEqual(1, 1, "broken (not actually)")


class TestAppBooleanPageTest(TestCase):
    def test_which_demonstrates_subtests(self):
        with self.subTest("Should return False"):
            false_response = self.client.get('/testapp/boolean/0/')
            self.assertEqual(false_response.content, b'False')
        with self.subTest("Should return True"):
            true_response = self.client.get('/testapp/boolean/1/')
            self.assertEqual(true_response.content, b'True')
        with self.subTest("Should return invalid"):
            PageInfo.objects.filter(page_title="fail").count()
            invalid_response = self.client.get('/testapp/boolean/99/')
            self.assertEqual(invalid_response.content, b'invalid')
