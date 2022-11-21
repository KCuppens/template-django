import factory.fuzzy

from apps.config.models import Config


class ConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Config

    key_name = factory.fuzzy.FuzzyText(length=12)
    title = factory.fuzzy.FuzzyText(length=48)
    value = factory.fuzzy.FuzzyText(length=48)
    description = factory.fuzzy.FuzzyText(length=48)
