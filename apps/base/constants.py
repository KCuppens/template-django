from django.utils.translation import gettext_lazy as _


ENVIRONMENT_COLORS = {
    "main": "#9c0000",
    "other": "#800080",
}

STATE_DRAFT = "draft"
# STATE_IN_REVIEW = 'in_review'
STATE_PUBLISHED = "published"
# STATE_CHANGES_REQUESTED = 'changes_requested'
# STATE_SCHEDULE = 'schedule'

STATES = [
    (STATE_DRAFT, _("Draft")),
    # (STATE_IN_REVIEW, 'In review'),
    (STATE_PUBLISHED, _("Published")),
    # (STATE_CHANGES_REQUESTED, 'Changes requested'),
    # (STATE_SCHEDULE, 'Schedule'),
]


COOKIE_NAME = "active_consents"
TYPE_FUNCTIONAL_AND_ESSENTIAL_COOKIES = "essential_functional_cookies"
TYPE_ANALYTICAL_COOKIES = "analytical_cookies"
TYPE_EXTERNAL_CONTENT_COOKIES = "external_content_cookies"

COOKIE_TYPES = (
    (TYPE_FUNCTIONAL_AND_ESSENTIAL_COOKIES, _("Essentiële en functionele cookies")),
    (TYPE_ANALYTICAL_COOKIES, _("Analytische cookies")),
    (TYPE_EXTERNAL_CONTENT_COOKIES, _("Cookies voor het tonen van externe inhoud")),
)
