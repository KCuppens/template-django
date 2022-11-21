from apps.base.utils import CustomGraphQLTestCase


class ContactTestCase(CustomGraphQLTestCase):
    def test_create_contact(self):
        response = self.query(
            """
            mutation createContact(
                $first_name: String!,
                $last_name: String!,
                $phone: String!,
                $message: String!,
                $email: String!) {
                createContact(
                    firstName: $first_name,
                    lastName: $last_name,
                    phone: $phone,
                    message: $message,
                    email: $email) {
                    verificationMessage
                }
            }
            """,
            variables={
                "first_name": "Test",
                "last_name": "Test",
                "phone": "Test",
                "message": "Test message",
                "email": "Test email",
            },
        )
        self.assertEqual(
            response.json()["data"]["createContact"]["verificationMessage"],
            "Thanks for contacting us. We will get back to you ASAP.",
        )
