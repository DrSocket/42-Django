"""Tests for ex00: the AJAX-only login/logout system."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountPageTests(TestCase):
    """The /account URL and the two behaviours it must have."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="s3cret-pass")

    def test_account_url_is_at_the_required_path(self):
        self.assertEqual(reverse("account:account"), "/account")
        self.assertEqual(self.client.get("/account").status_code, 200)

    def test_anonymous_visitor_gets_the_login_form(self):
        response = self.client.get("/account")
        self.assertContains(response, 'id="login-form"')
        self.assertNotContains(response, "Logged as")

    def test_logged_in_visitor_gets_the_required_text_and_a_logout_button(self):
        self.client.force_login(self.user)
        response = self.client.get("/account")
        # The subject asks for this exact wording.
        self.assertContains(response, "Logged as alice")
        self.assertContains(response, 'id="logout-form"')
        self.assertNotContains(response, 'id="login-form"')

    def test_state_survives_a_manual_refresh(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.get("/account"), "Logged as alice")
        # A second identical request is what a manual refresh sends.
        self.assertContains(self.client.get("/account"), "Logged as alice")


class LoginEndpointTests(TestCase):
    """The login endpoint answers AJAX POSTs with JSON."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="s3cret-pass")
        self.url = reverse("account:login")

    def test_valid_credentials_log_the_user_in(self):
        response = self.client.post(
            self.url, {"username": "alice", "password": "s3cret-pass"}
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["authenticated"])
        self.assertIn("Logged as alice", payload["html"])
        self.assertIn("_auth_user_id", self.client.session)

    def test_invalid_credentials_return_the_form_with_its_errors(self):
        response = self.client.post(
            self.url, {"username": "alice", "password": "wrong-password"}
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["authenticated"])
        # The error has to be renderable on the page.
        self.assertIn("login-form", payload["html"])
        self.assertIn("errors", payload["html"])
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_empty_submission_returns_field_errors(self):
        payload = self.client.post(self.url, {}).json()
        self.assertFalse(payload["authenticated"])
        self.assertIn("This field is required.", payload["html"])

    def test_get_is_rejected(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class LogoutEndpointTests(TestCase):
    """The logout endpoint answers AJAX POSTs with JSON."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="s3cret-pass")
        self.url = reverse("account:logout")

    def test_post_logs_the_user_out_and_returns_the_form(self):
        self.client.force_login(self.user)
        payload = self.client.post(self.url).json()
        self.assertFalse(payload["authenticated"])
        self.assertIn("login-form", payload["html"])
        self.assertNotIn("Logged as", payload["html"])
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_get_is_rejected(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_csrf_token_is_required(self):
        """The endpoint is protected: it is not csrf_exempt."""
        self.client.force_login(self.user)
        csrf_client = self.client_class(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(self.url).status_code, 403)
