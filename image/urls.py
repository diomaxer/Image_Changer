from django.urls import path
from .views import home_page_view, change_image_view, add_image

urlpatterns = [
    path('', home_page_view, name='home'),
    path('add_image/', add_image, name='add'),
    path('change_image/', change_image_view, name='change'),
]