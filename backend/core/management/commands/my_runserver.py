from django.conf import settings
from django.core.management.commands.runserver import Command as runServer


class Command(runServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_addr = settings.SERVER_HOST
        self.default_port = settings.SERVER_PORT

    def inner_run(self, *args, **options):
        self.stdout.write(
            f'-------------------------------------\n'
            f'DEBUG = {settings.DEBUG}\n'
            f'admin panel = {"on" if settings.DJANGO_ADMIN else "off"}\n'
            f'db name = {settings.DJANGO_DB_NAME}\n'
            f'lang = {settings.LANGUAGE_CODE}\n'
            f'host = {self.default_addr}\n'
            f'port = {self.default_port}\n'
            f'-------------------------------------\n'
        )
        super().inner_run(*args, **options)
