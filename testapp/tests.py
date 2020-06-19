from unittest import skip, expectedFailure
from django.test import TestCase
from django.urls import reverse
from .models import PageInfo


class TestWhichReportsVariousStatuses(TestCase):
    def test_will_report_failed(self):
        PageInfo.objects.filter(page_title="fail").count()
        response = self.client.get('/testapp/missing')
        self.assertEqual(response.status_code, 200)

    @expectedFailure
    def test_unexpected_success_will_report_failed(self):
        self.assertEqual(1, 1, "broken (not actually)")

    # pylint: disable=unreachable
    def test_will_report_error(self):
        PageInfo.objects.filter(page_title="error").count()
        url = reverse('about')
        response = self.client.get(url)
        raise Exception
        self.assertEqual(response.status_code, 200)

    @skip("demonstrating skipping")
    def test_will_report_waived(self):
        self.fail("shouldn't have run")

    def test_will_report_passed(self):
        PageInfo.objects.filter(page_title="pass").count()
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @expectedFailure
    def test_expected_failure_will_report_passed(self):
        self.assertEqual(1, 0, "broken")

    def test_with_subtests_will_report_failed(self):
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

    def test_with_subtests_will_report_passed(self):
        with self.subTest("Should pass"):
            PageInfo.objects.filter(page_title="pass").count()
            self.assertEqual(1, 1)
