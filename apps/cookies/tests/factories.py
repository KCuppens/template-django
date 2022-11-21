import factory.fuzzy

from apps.cookies.models import Cookie


class CookieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cookie

    title = factory.fuzzy.FuzzyText(length=12)
    message = factory.fuzzy.FuzzyText(length=48)
    essential_functional_cookies_description = factory.fuzzy.FuzzyText(length=48)
    analytical_cookies_description = factory.fuzzy.FuzzyText(length=48)
    external_content_cookies_description = factory.fuzzy.FuzzyText(length=48)
