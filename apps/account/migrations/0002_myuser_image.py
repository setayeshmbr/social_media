# Generated by Django 3.2 on 2021-04-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photo', verbose_name='Image'),
        ),
    ]