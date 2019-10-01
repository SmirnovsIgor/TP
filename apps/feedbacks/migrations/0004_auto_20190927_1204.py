# Generated by Django 2.2.4 on 2019-09-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbacks', '0003_auto_20190925_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(choices=[('OK', 'ok'), ('SUSPICIOUS', 'suspicious'), ('DELETED', 'deleted'), ('CANCELED', 'canceled')], default='OK', max_length=16),
        ),
    ]
