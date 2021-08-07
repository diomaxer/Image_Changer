from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render

import requests as r
import uuid

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
            resp = r.get(link)
            file_ext = resp.headers.get('Content-Type').split('/')[1]
            file_name = settings.BASE_DIR / 'media/media' / (str(uuid.uuid4()) + "." + file_ext)
            with open(file_name, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=128):
                    f.write(chunk)
            Image.objects.create(image=f.name)
            return HttpResponsePermanentRedirect("/change_image")
    else:
        form = ImageForm()
    return render(request, 'image/add_image.html', {'form': form})


def change_image_view(request):
    image = Image.objects.latest('id')
    if request.method == 'POST':
        width = request.POST['width']
        height = request.POST['height']
        image.resized_img(width=int(width), height=int(height))
    context = {
        'image': image
    }
    return render(request, 'image/change_image.html', context)
