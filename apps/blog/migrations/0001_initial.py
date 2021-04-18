# Generated by Django 3.2 on 2021-04-18 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category_images', verbose_name='Image')),
                ('cropping', image_cropping.fields.ImageRatioField('image', '900x874', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(allow_unicode=True, blank=True, editable=False, populate_from=['title'], unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, verbose_name='Title')),
                ('image', models.ImageField(upload_to='uploaded_images', verbose_name='Image')),
                ('cropping', image_cropping.fields.ImageRatioField('image', '900x750', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping')),
                ('caption', models.CharField(blank=True, max_length=1024, verbose_name='Caption')),
                ('location', models.TextField(blank=True, verbose_name='Location')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('a', 'Archive'), ('p', 'Publish')], max_length=2, verbose_name='Publish status')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(blank=True, null=True, related_name='posts', to='blog.Category', verbose_name='Category')),
            ],
        ),
    ]
