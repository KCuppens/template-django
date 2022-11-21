from django.test import TestCase

from apps.config.models import Config
from apps.config.tests.factories import ConfigFactory


class ConfigManagerTestCase(TestCase):
    def setUp(self):
        self.config = ConfigFactory()

    def test_get_config(self):
        self.assertEqual(
            self.config.value,
            Config.objects.get_config(self.config.key_name),
        )
