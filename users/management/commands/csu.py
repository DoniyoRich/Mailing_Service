from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not CustomUser.objects.filter(email='admin@mail.com').exists():
            username = 'admin'
            email = 'admin@mail.com'
            password = '123'
            first_name = 'admin'
            last_name = 'admin'
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(self.style.SUCCESS(f'Админ создан! Логин: {email}, пароль: {password}'))
