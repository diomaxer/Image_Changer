# Generated by Django 3.2.6 on 2021-08-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0004_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Картинка'),
        ),
    ]