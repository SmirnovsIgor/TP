# Generated by Django 2.2.4 on 2019-09-03 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20190826_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='flat',
        ),
        migrations.AddField(
            model_name='address',
            name='apartments',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='house',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
