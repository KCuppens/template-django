from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase

from apps.base.utils import CustomGraphQLTestCase
from apps.users.tests.factories import UserFactory
from apps.users.tokens import account_activation_token


class UserTestCase(JSONWebTokenTestCase):
    fixtures = ["Group.json"]

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        return UserFactory(is_staff=True)

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_group(self):
        return Group.objects.filter(name="Admin").first()

    def setUp(self):
        self.administrator = self.create_user()
        self.group = self.create_group()
        self.administrator.groups.add(self.group)
        self.client.authenticate(self.administrator)

    @mock.patch("apps.users.schemas.schema.send_email.delay")
    def test_reset_password(self, send_email):
        query = """
            mutation resetPassword($email: String!) {
                resetPassword(email: $email) {
                    verificationMessage
                }
            }
            """
        variables = {"email": self.administrator.email}
        response = self.client.execute(query, variables)
        send_email.assert_called_once()
        self.assertEqual(
            response.data["resetPassword"]["verificationMessage"],
            "A password reset link was sent to your email address.",
        )

    def test_reset_password_confirm(self):
        token = account_activation_token.make_token(self.administrator)
        uid = urlsafe_base64_encode(force_bytes(self.administrator.pk))
        query = """
            mutation resetPasswordConfirm(
                $uidb64: String!, $token: String!, $password: String!) {
                resetPasswordConfirm(
                    uidb64: $uidb64, token: $token, password: $password) {
                    verificationMessage
                }
            }
            """
        variables = {
            "uidb64": uid,
            "token": token,
            "password": "test12345",
        }
        response = self.client.execute(query, variables)
        self.assertEqual(
            response.data["resetPasswordConfirm"]["verificationMessage"],
            "Password has been succesfully resetted.",
        )


class UserAuthTestCase(CustomGraphQLTestCase):
    fixtures = ["Group.json"]

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_user(self):
        return get_user_model().objects.create_user(
            username="test@{app_name}.be",
            email="test@{app_name}.be",
            password="dolphins",
            is_staff=True,
        )

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_group(self):
        return Group.objects.create(name="testgroup")

    def setUp(self):
        self.administrator = self.create_user()
        self.group = self.create_group()

    def test_register_user(self):
        response = self.query(
            """
            mutation registerUser(
                $first_name: String!,
                $last_name: String!,
                $email: String!,
                $password: String!) {
                registerUser(
                    firstName: $first_name,
                    lastName: $last_name,
                    email: $email,
                    password: $password) {
                    user{
                        id
                    },
                    verificationMessage
                }
            }
            """,
            variables={
                "first_name": "Test",
                "last_name": "Test",
                "email": "new@{app_name}.be",
                "password": "test123",
            },
        )
        self.assertTrue(response.json()["data"]["registerUser"]["user"]["id"])
        self.assertEqual(
            response.json()["data"]["registerUser"]["verificationMessage"],
            "Successfully created user, Test Test",
        )

    def test_activate_user(self):
        token = account_activation_token.make_token(self.administrator)
        uid = urlsafe_base64_encode(force_bytes(self.administrator.pk))
        response = self.query(
            """
            mutation activateUser($uid: String!, $token: String!) {
                activateUser(uid: $uid, token: $token) {
                    verificationMessage
                }
            }
            """,
            variables={"token": token, "uid": uid},
        )
        self.assertEqual(
            response.json()["data"]["activateUser"]["verificationMessage"],
            "The user has been activated.",
        )

    def test_login_user(self):
        self.client.logout()
        self.administrator.is_active = True
        self.administrator.save(update_fields=["is_active"])
        response = self.query(
            """
            mutation loginUser($email: String!, $password: String!) {
                loginUser(email: $email, password: $password) {
                    verificationMessage
                }
            }
            """,
            variables={"email": "test@{app_name}.be", "password": "dolphins"},
        )
        self.assertEqual(
            response.json()["data"]["loginUser"]["verificationMessage"],
            "You logged in successfully.",
        )
