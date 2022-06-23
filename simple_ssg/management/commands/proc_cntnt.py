from django.core.management.base import BaseCommand
from django.utils import timezone

from ...content import Content

class Command(BaseCommand):
    help = 'Processes the Kramdown contenzt'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        
        mycnt = Content()
        
        mycnt.handle_content()


