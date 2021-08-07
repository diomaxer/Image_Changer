from django.db import models
from PIL import Image as ImagePIL
import os


class Image(models.Model):
    image = models.ImageField(verbose_name='Фаил', null=True, blank=True, upload_to='media')

    def __str__(self):
        return str(self.id)

    def resized_img(self, width, height):
        img = ImagePIL.open(self.image.path)
        resized_img = img.resize((width, height), ImagePIL.ANTIALIAS)
        resized_img.save(self.image.path)
