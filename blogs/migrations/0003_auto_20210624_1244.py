# Generated by Django 3.1.7 on 2021-06-24 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_blogpost_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/', verbose_name='Upload Picture'),
        ),
    ]