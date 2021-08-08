from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render


import requests as r
import uuid
import shutil

from django.core.validators import URLValidator

from .models import Image
from .forms import ImageForm


def home_page_view(request):
    images = Image.objects.all()
    context = {
        'images': images
    }
    return render(request, 'home.html', context)


def add_image(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        link = request.POST['link']
        form = ImageForm(request.POST, request.FILES)
        picture = form.has_changed()
        if link and picture:
            form = ImageForm()
            return render(request, 'image/add_image.html', {
                'form': form,
                'error': 'Выберите, что-то одно'
            })
        if not link and not picture:
            form = ImageForm()
            return render(request, 'image/add_image.html', {
                'form': form,
                'error': 'Введите, одно поле'
            })
        if not link and picture:
            if form.is_valid():
                form.save()
                return HttpResponsePermanentRedirect("/change_image")
        if link and not picture:
            try:
                resp = r.get(link)
            except:
                return render(request, 'image/add_image.html', {
                    'form': form,
                    'error': 'Данная ссылка не корректна',
                })
            file_ext = resp.headers.get('Content-Type').split('/')[1]
            if file_ext in ['png', 'jpeg', 'jpg']:
                file_name = settings.BASE_DIR / 'media/media' / (str(uuid.uuid4()) + "." + file_ext)
                with open(file_name, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=128):
                        f.write(chunk)
                Image.objects.create(image=f.name)
                return HttpResponsePermanentRedirect("/change_image")
            else:
                form = ImageForm()
                return render(request, 'image/add_image.html', {'form': form,
                                                                'error': 'Неверный формат. Разрешённые форматы: jpg, jpeg, png',
                                                                })
    else:
        form = ImageForm()
    return render(request, 'image/add_image.html', {'form': form})


def change_image_view(request):
    image = Image.objects.latest('id')
    error = None
    if request.method == 'POST':
        width = request.POST['width'] or None
        height = request.POST['height'] or None
        if width is None and height is None:
            return render(request, 'image/change_image.html', {
                'image': image,
                'error': 'Заполните хотя бы одно поле',
            })
        if width is not None:
            width = int(width)
            if width <= 0:
                error = 'Ширина меньше или ровна нулю'
            if width > 1920:
                error = 'Ширина не может быть больше 1920'
        if height is not None:
            height = int(height)
            if height <= 0:
                error = 'Высота меньше или ровна нулю'
            if height > 1080:
                error = 'Высота не может быть больше 1080'
        if error is not None:
            return render(request, 'image/change_image.html', {
                'image': image,
                'error': error,
            })
        new_image = shutil.copyfile(image.image.path, settings.BASE_DIR / 'media/media' / (str(uuid.uuid4()) + ".png"))
        with open(new_image) as f:
            f.close()
            Image.objects.create(image=f.name)
        image.resized_img(width=width, height=height)
    context = {
        'image': image
    }
    return render(request, 'image/change_image.html', context)
