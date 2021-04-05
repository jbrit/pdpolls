from django.core.management.base import BaseCommand
from core.models import Category


class Command(BaseCommand):
    help = 'Add Categories'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Name of the \'.txt\' you want to create from')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        with open(f"{filename}.txt") as file:
            for num, line in enumerate(file):
                cat = Category(name=line.strip(), order=num+1)
                cat.save()