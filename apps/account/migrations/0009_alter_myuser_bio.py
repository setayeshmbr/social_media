# Generated by Django 3.2 on 2021-04-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_myuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='bio',
            field=models.CharField(blank=True, max_length=100, verbose_name='Bio'),
        ),
    ]