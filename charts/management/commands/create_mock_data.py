# charts/management/commands/create_mock_data.py

from django.core.management.base import BaseCommand
from charts.models import Application
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate 100 mock applications data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        application_types = ['emergency', 'planned', 'superfix']

        # Create 100 mock applications
        for _ in range(100):
            Application.objects.create(
                owner_name=fake.name(),
                date_of_register=fake.date_this_decade(),
                application_type=random.choice(application_types)
            )

        self.stdout.write(self.style.SUCCESS('Successfully created 100 mock application records'))
