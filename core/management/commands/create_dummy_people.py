from django.core.management.base import BaseCommand
from core.models import Category, VoteItem


class Command(BaseCommand):
    help = 'Add People'

    """def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Name of the \'.txt\' you want to create from')"""

    def handle(self, *args, **kwargs):
        cats = Category.objects.all()
        for num, cat in enumerate(cats):
            for i in range(1, 5):
                item = VoteItem(name=f"Dummy Item {num} {i}", category=cat)
                item.save()