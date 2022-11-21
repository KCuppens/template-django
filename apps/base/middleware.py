from __future__ import unicode_literals

from copy import deepcopy

from django.apps import apps
from django.conf import settings
from django.urls import Resolver404, resolve
from django.utils.deprecation import MiddlewareMixin


class AdminModelOverrideMiddleware(MiddlewareMixin):
    def init_config(self, request, app_list):
        self.request = request
        self.app_list = app_list
        self.config = getattr(settings, "ADMIN_MODEL_OVERRIDE", {})
        self.models = self.get_all_models()
        self.app_list = self.override_config()
        self.app_list = self.sort_app_list_based_on_config()
        self.app_list = self.sort_models_list_based_config()

    def get_all_models(self):
        # Flatten all models from apps
        models = []
        for app in self.app_list:
            for model in app["models"]:
                models.append(self.get_model_name(app["app_label"], model["object_name"]))
        return models

    def get_model_name(self, app_name, model_name):
        if "." not in model_name:
            model_name = "%s.%s" % (app_name, model_name)
        return model_name

    def get_sortable_config(self):
        config = deepcopy(self.config)
        for conf in config:
            if "position" not in conf:
                config.remove(conf)
        config = sorted(config, key=lambda k: k["position"])
        config = [c["app"] for c in config]
        return config

    def sort_models_list_based_config(self):
        app_list = deepcopy(self.app_list)
        for app in app_list:
            if "models" in app:
                app["models"] = self.sort_model_list(app["app_label"], app["models"])
        return app_list

    def sort_model_list(self, app_name, model_list):
        config_models = self.get_config_models_by_app_name(app_name)
        model_list, popped_list = self.pop_models_from_model_list(model_list, config_models)
        popped_list = self.sort_popped_model_list_by_config(popped_list, config_models)
        return popped_list + model_list

    def sort_popped_model_list_by_config(self, popped_list, config_models):
        sorted_list = []
        for model in config_models:
            for popped in popped_list:
                if popped["object_name"] == model:
                    sorted_list.append(popped)
                    continue
        return sorted_list

    def pop_models_from_model_list(self, model_list, config):
        clone = deepcopy(model_list)
        popped_list = []
        for model in model_list:
            if model["object_name"] in config:
                popped_list.append(model)
                clone.remove(model)
        return clone, popped_list

    def get_config_models_by_app_name(self, app_name):
        for app in self.config:
            if app["app"] == app_name:
                return [model.split(".")[1] for model in app["models"]]
        return []

    def sort_app_list_based_on_config(self):
        config = self.get_sortable_config()
        app_list, popped_list = self.pop_apps_from_app_list(config)
        popped_list = self.sort_popped_list_by_config(popped_list, config)
        return popped_list + app_list

    def sort_popped_list_by_config(self, popped_list, config):
        sorted_list = []
        for app in config:
            for popped in popped_list:
                if popped["app_label"] == app:
                    sorted_list.append(popped)
                    continue
        return sorted_list

    def pop_apps_from_app_list(self, config):
        app_list = deepcopy(self.app_list)
        popped_list = []
        for app in self.app_list:
            if app["app_label"] in config:
                popped_list.append(app)
                app_list.remove(app)
        return app_list, popped_list

    def override_config(self):
        if not self.config:
            return self.app_list
        app_list = deepcopy(self.app_list)
        for app_config in self.config:
            # Check if app exists in the app_list
            app_exists = self.check_app_exists(app_config)
            if app_exists:
                if "delete" in app_config:
                    app_list.remove(app_exists)
                    continue
                else:
                    # Override label of the app
                    app_list = self.override_app_label(app_list, app_config)
                    # Get all the models that are not yet in the correct app according to config
                    non_existent_models = self.check_model_already_in_app(app_config, app_exists)
                    # Check if non_existent_models is not empty and if they exist in app_list
                    if non_existent_models:
                        non_existent_models = self.check_model_exists_in_app(non_existent_models)
                        # If they exist add them in the correct app in the app_list
                        app_list = self.make_app_list(app_list, app_config, non_existent_models)
        return app_list

    def override_app_label(self, app_list, app_config):
        for app in app_list:
            if app["app_label"] == app_config["app"]:
                app["name"] = app_config["labels"]
        return app_list

    def make_app_list(self, app_list, app_config, non_existent_models):
        for app in app_list:
            if app["app_label"] == app_config["app"]:
                for model in non_existent_models:
                    app["models"].append(self.get_model_dict(model))
                    # Remove the model from their previous app
                    app_list = self.remove_model_from_app_list(app_list, model)
        return app_list

    def remove_model_from_app_list(self, app_list, model):
        for app in app_list:
            if app["app_label"] == model.split(".")[0]:
                count = len(app["models"])
                if count <= 1:
                    app_list.remove(app)
                    return app_list
                else:
                    for model_dict in app["models"]:
                        if model_dict["object_name"] == model.split(".")[1]:
                            app["models"].remove(model_dict)
                    return app_list

    def get_model_dict(self, model):
        splitted_model = model.split(".")
        model = apps.get_model(model)
        app_name = splitted_model[0]
        model_lowercase = model._meta.object_name.lower()
        return {
            "model": model,
            "name": model.__name__,
            "object_name": model._meta.object_name,
            "perms": {"add": True, "change": True, "delete": True, "view": True},
            "admin_url": f"/admin/{app_name}/{model_lowercase}/",
            "add_url": f"/admin/{app_name}/{model_lowercase}/add/",
            "view_only": False,
        }

    def check_model_exists_in_app(self, non_existent_models):
        for model in non_existent_models:
            if model not in self.models:
                non_existent_models.remove(model)
        return non_existent_models

    def check_app_exists(self, app_config):
        for app_name in self.app_list:
            if app_config["app"] == app_name["app_label"]:
                return app_name
        return False

    def check_model_already_in_app(self, app_config, app):
        current_models = []
        for model in app["models"]:
            current_models.append(self.get_model_name(app["app_label"], model["object_name"]))
        return list(set(current_models) ^ set(app_config["models"]))

    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            return response
        if not url.app_name == "admin":
            # current view is not a django admin index
            # or app_list view, bail out!
            return response
        if "app_list" in response.context_data:
            app_list = response.context_data["app_list"]
        elif "available_apps" in response.context_data:
            app_list = response.context_data["available_apps"]
        else:
            return response

        self.init_config(request, app_list)
        ordered_app_list = self.app_list
        if "app_list" in response.context_data:
            response.context_data["app_list"] = ordered_app_list
        elif "available_apps" in response.context_data:
            response.context_data["available_apps"] = ordered_app_list
        return response
