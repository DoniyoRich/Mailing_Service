from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Удаляет миграции пользователей"

    def handle(self, *args, **options):
        call_command('migrate', ['auth', 'zero'])
        self.stdout.write(self.style.SUCCESS('Успешно произведен откат миграций приложения auth'))
