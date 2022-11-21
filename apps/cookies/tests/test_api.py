import pytest

from apps.base.utils import CustomGraphQLTestCase
from apps.cookies.tests.factories import CookieFactory


class CookieTestcase(CustomGraphQLTestCase):
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def create_cookie(self):
        return CookieFactory()

    def setUp(self):
        self.cookie = self.create_cookie()

    def test_get_cookie(self):
        response = self.query(
            """
            query getCookie{
                getCookie{
                    title,
                    message,
                    essentialFunctionalCookiesDescription,
                    analyticalCookiesDescription,
                    externalContentCookiesDescription
                }
            }
            """
        )
        self.assertEqual(response.json()["data"]["getCookie"]["title"], self.cookie.title)
        self.assertEqual(response.json()["data"]["getCookie"]["message"], self.cookie.message)
        self.assertEqual(
            response.json()["data"]["getCookie"]["essentialFunctionalCookiesDescription"],
            self.cookie.essential_functional_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["analyticalCookiesDescription"],
            self.cookie.analytical_cookies_description,
        )
        self.assertEqual(
            response.json()["data"]["getCookie"]["externalContentCookiesDescription"],
            self.cookie.external_content_cookies_description,
        )
