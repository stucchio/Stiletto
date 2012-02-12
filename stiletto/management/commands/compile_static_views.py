from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.importlib import import_module


class Command(BaseCommand):
    args = '<output_path>'
    help = 'Precompiles static views.'

    def handle(self, *args, **kwargs):
        if len(args) == 1:
            output_path = args[0]
        else:
            output_path = settings.STATIC_VIEW_FOLDER
        static_mapper = import_module(settings.ROOT_URLCONF).static_urlpatterns
        static_mapper.render(output_path)

