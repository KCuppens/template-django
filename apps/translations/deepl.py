from django.conf import settings

import deepl


class Deepl:
    def __init__(self):
        self.api_key = settings.DEEPL_API_KEY
        self.translator = deepl.Translator(self.api_key)
        self.default = "nl"

    def translate(self, text, target_lang):
        if self.translator:
            return self.translator.translate_text(
                text,
                target_lang=get_target_language(target_lang),
                source_lang=self.default,
                preserve_formatting=True,
            )


def get_target_language(target_lang):
    langs = {"fr": "fr", "en": "EN-US"}
    return langs[target_lang]
