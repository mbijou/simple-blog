from django.contrib.messages.api import get_messages
from django.contrib.messages.constants import DEFAULT_LEVELS
from django.conf import settings
from django.urls import translate_url
from django.urls import reverse_lazy


def languages(request):
    languages_list = []

    for language_code, language_name in settings.LANGUAGES:
        languages_list.append((language_code, language_name, translate_url(str(request.path), language_code)))

    return {
        'languages': languages_list,
    }
