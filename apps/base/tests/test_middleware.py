from unittest.mock import Mock

from django.conf import settings
from django.test import TestCase

from apps.base.middleware import AdminModelOverrideMiddleware


class MyMiddlewareTestCase(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.session = {}
        self.mm = AdminModelOverrideMiddleware(self.request)
        self.mm.init_config(self.request, [])

    def test_get_all_models(self):
        models = self.mm.get_all_models()
        self.assertEqual(len(models), 0)

    def test_get_model_name(self):
        self.assertEqual(self.mm.get_model_name("product", "Product"), "product.Product")

    def test_get_sortable_config(self):
        config = self.mm.get_sortable_config()
        if settings.ADMIN_MODEL_OVERRIDE:
            self.assertGreater(len(config), 0)
        else:
            self.assertEqual(len(config), 0)

    def test_get_config_models_by_app_name(self):
        config = self.mm.get_config_models_by_app_name("blog")
        if settings.ADMIN_MODEL_OVERRIDE:
            self.assertGreater(len(config), 0)
        else:
            self.assertEqual(len(config), 0)

    def test_sort_app_list_based_on_config(self):
        config = self.mm.sort_app_list_based_on_config()
        self.assertEqual(len(config), 0)

    def test_pop_apps_from_app_list(self):
        config = self.mm.pop_apps_from_app_list(settings.ADMIN_MODEL_OVERRIDE or {})
        if settings.ADMIN_MODEL_OVERRIDE:
            self.assertGreater(len(config), 0)
        else:
            self.assertEqual(len(config), 0)

    def test_override_config(self):
        config = self.mm.override_config()
        self.assertEqual(len(config), 0)

    def test_get_model_dict(self):
        config = self.mm.get_model_dict("blog.Blog")
        self.assertGreater(len(config), 0)

    def test_check_app_exists(self):
        config = self.mm.check_app_exists(settings.ADMIN_MODEL_OVERRIDE or {})
        self.assertFalse(config)
