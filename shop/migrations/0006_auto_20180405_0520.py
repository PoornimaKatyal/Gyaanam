# Generated by Django 2.0.3 on 2018-04-05 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20180404_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='books',
            name='genre',
        ),
        migrations.AddField(
            model_name='books',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, to='shop.Genre'),
        ),
    ]
