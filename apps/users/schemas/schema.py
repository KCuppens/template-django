import logging

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import Group, Permission

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt import ObtainJSONWebToken, Refresh, Verify
from graphql_jwt.decorators import login_required, permission_required
from graphql_jwt.utils import jwt_encode, jwt_payload

from apps.base.utils import model_to_dict
from apps.mail.tasks import send_email
from apps.users.utils import decode_token


logger = logging.getLogger(__name__)


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission
        fields = "__all__"


class Query(graphene.ObjectType):
    get_user_detail = graphene.Field(UserType, id=graphene.String())

    @login_required
    @permission_required("users.view_user")
    def resolve_get_user_detail(self, info, id):
        user = User.objects.filter(id=id).first()
        logger.info(f"Get user: {model_to_dict(user)}")
        return user


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)
    verification_message = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        password = kwargs.get("password")
        email = kwargs.get("email")
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
        )
        user.set_password(password)
        user.save()

        verification_message = f"Successfully created user, {user}"

        activation_link = user.get_activation_link()
        logger.info(
            f"User registered: {model_to_dict(user)} and activation link: {activation_link}"
        )
        # TODO create send_activation_email email
        send_email.delay(
            "send_activation_email",
            str(user),
            user.email,
            {"{activation_link}": activation_link},
        )
        return RegisterUser(user=user, verification_message=verification_message)


class ActivateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    verification_message = graphene.String()

    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        uid = kwargs.get("uid")
        token = kwargs.get("token")
        check, user = decode_token(uid, token)
        if check:
            user.is_active = True
            user.save(update_fields=["is_active"])
            logger.info(f"User activated: {model_to_dict(user)}")
            verification_message = "The user has been activated."
        else:
            verification_message = "The user is already activated."
        return ActivateUser(user=user, verification_message=verification_message)


class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    verification_message = graphene.String()
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        if info.context.user.is_authenticated:
            logger.info(f"User already logged in: {model_to_dict(info.context.user)}")
            raise GraphQLError("The user is already logged in.")

        user = authenticate(username=email, password=password)
        if user:
            login(info.context, user)
            payload = jwt_payload(user)
            token = jwt_encode(payload)
            logger.info(
                f"User logged in: {model_to_dict(user)} with token: {token} and payload: {payload}"
            )
            verification_message = "You logged in successfully."
            return LoginUser(
                user=user,
                token=token,
                verification_message=verification_message,
            )
        else:
            user_exists = User.objects.get(email=email)
            if user_exists.is_active:
                logger.info(f"Invalid login credentials: {model_to_dict(user)}")
                verification_message = "Invalid login credentials."
                raise GraphQLError(verification_message=verification_message)
            else:
                logger.info(f"Email not verified: {model_to_dict(user)}")
                verification_message = "Your email is not verified."
                raise GraphQLError(verification_message=verification_message)


class LogoutUser(graphene.Mutation):
    verification_message = graphene.String()
    is_logged_out = graphene.Boolean()

    @login_required
    def mutate(self, info, **kwargs):
        logout(info.context)
        return LogoutUser(
            is_logged_out=True,
            verification_message="User successfully logged out!",
        )


class ResetPassword(graphene.Mutation):
    reset_link = graphene.String()
    verification_message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        if email.strip() == "":
            raise GraphQLError("Email can't be blank.")

        user = User.objects.filter(email=email).first()
        if user is None:
            raise GraphQLError("User with the provided email was not found.")

        password_reset_link = user.get_password_reset_link()
        logger.info(
            f"Reset password initiated: {model_to_dict(user)} "
            f"with password reset link: {password_reset_link}"
        )
        # TODO create reset_password_email
        send_email.delay(
            "reset_password_email",
            str(user),
            user.email,
            {"{password_reset_link}": password_reset_link},
        )
        return ResetPassword(
            reset_link=password_reset_link,
            verification_message=("A password reset link was sent to your email address."),
        )


class ResetPasswordConfirm(graphene.Mutation):
    verification_message = graphene.String()
    is_valid = graphene.Boolean()

    class Arguments:
        uidb64 = graphene.String()
        token = graphene.String()
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")
        password = kwargs.get("password")

        check, user = decode_token(uidb64, token)
        if check and user:
            user.set_password(password)
            user.save()
            logger.info(f"Reset password confirmed: {model_to_dict(user)}")
        return ResetPasswordConfirm(
            is_valid=False,
            verification_message="Password has been succesfully resetted.",
        )


class ChangePassword(graphene.Mutation):
    user = graphene.Field(UserType, token=graphene.String(required=True))
    verification_message = graphene.String()

    class Arguments:
        password = graphene.String(required=True)
        confirm_password = graphene.String(required=True)

    @login_required
    @permission_required("users.change_user")
    def mutate(self, info, **kwargs):
        password = kwargs.get("password")
        confirm_password = kwargs.get("confirm_password")

        if password != confirm_password:
            raise GraphQLError("Password and Confirm Passowrd do not match!")

        user = info.context.user
        if user:
            user.set_password(password)
            user.save()
            logger.info(f"Password changed: {model_to_dict(user)}")
            return ChangePassword(
                user=user,
                verification_message=("Password has been changed successfully!"),
            )
        raise GraphQLError("User is not logged in, please login to proceed!")


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    activate_user = ActivateUser.Field()

    login_user = LoginUser.Field()
    logout_user = LogoutUser.Field()
    reset_password = ResetPassword.Field()
    reset_password_confirm = ResetPasswordConfirm.Field()
    change_password = ChangePassword.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
