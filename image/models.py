import uuid

from django.db import models
from PIL import Image as ImagePIL
from django.core.files.storage import default_storage

from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Image(models.Model):
    image = models.ImageField(verbose_name='Фаил', null=True, blank=True, upload_to='media')

    def __str__(self):
        return str(self.id)


    def resized_img(self, width, height):
        img = ImagePIL.open(self.image.path)
        (original_width, original_height) = img.size
        if width is None:
            width = int((original_height * height) / original_width)
        if height is None:
            height = int((original_width * width) / original_height)
        resized_img = img.resize((width, height), ImagePIL.ANTIALIAS)
        resized_img.save(self.image.path)
