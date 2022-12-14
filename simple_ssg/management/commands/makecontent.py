from django.core.management.base import BaseCommand
from django.utils import timezone

from ...content import Content

class Command(BaseCommand):
    help = 'Processes the Kramdown contenzt'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', type=str)


    def handle(self, *args, **options):
        print(options)
        default_mode = 'django'
        if (mode := options['mode']) is None:
            mode = default_mode
        elif not (mode in ['django', 'static']):
            mode = default_mode
        


        time = timezone.now().strftime('%X')
        self.stdout.write(f"It's now {time} and running mode: {mode}")
        
        mycnt = Content(mode=mode)
        
        mycnt.handle_content()


