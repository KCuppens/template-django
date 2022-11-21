import logging

import graphene
from graphene_django import DjangoObjectType

from apps.base.utils import model_to_dict
from apps.contact.models import Contact
from apps.mail.tasks import send_email


logger = logging.getLogger(__name__)


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = "__all__"


class CreateContact(graphene.Mutation):
    contact = graphene.Field(ContactType)
    verification_message = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone = graphene.String(required=True)
        message = graphene.String()
        email = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        first_name = kwargs.get("first_name", None)
        last_name = kwargs.get("last_name", None)
        phone = kwargs.get("phone", None)
        message = kwargs.get("message", None)
        email = kwargs.get("email", None)

        contact = Contact.objects.create(
            first_name=first_name, last_name=last_name, phone=phone, message=message, email=email
        )
        logger.info(f"Create contact: {model_to_dict(contact)}")
        # TODO create send_admin_email email
        send_email.delay(
            "send_admin_email",
            "Admin",
            email,
            {
                "{first_name}": first_name,
                "{last_name}": last_name,
                "{phone}": phone,
                "{message}": message,
                "{email}": email,
            },
        )
        # TODO create send_client_email email
        send_email.delay(
            "send_client_email",
            f"{first_name} {last_name}",
            email,
            {
                "{first_name}": first_name,
                "{last_name}": last_name,
                "{phone}": phone,
                "{message}": message,
                "{email}": email,
            },
        )
        verification_message = "Thanks for contacting us. We will get back to you ASAP."
        return CreateContact(contact=contact, verification_message=verification_message)


class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
