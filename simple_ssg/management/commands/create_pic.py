from django.core.management.base import BaseCommand
from django.utils import timezone
import os
import PIL
import string
from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps
from pathlib import Path


class Command(BaseCommand):
    help = 'Processes the Kramdown contenzt'

    FONTS_PATH = Path('~/Library/Fonts')
    TARGET_PATH = Path('./CONTENT/assets/images/products')

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)


 

        width, height = 128, 128

        text = 'SOP-8'
        font_size = 28

        
        img = Image.new("RGBA", (width, height), color='#000044AA')   # "L": (8-bit pixels, black and white)
        font = ImageFont.truetype(str(self.FONTS_PATH / "RobotoMono-Regular.ttf"), font_size)
        draw = ImageDraw.Draw(img)
        draw.text(((width)/2, (height)/2), text=text, fill='white', font=font, anchor="mm", align='center')

        img.save(str(self.TARGET_PATH / str(text + '.png')))