# Generated by Django 2.0.3 on 2018-03-31 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/%Y/%m/%D/'),
        ),
    ]
