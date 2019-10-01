# Generated by Django 2.2.4 on 2019-08-23 11:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(blank=True, max_length=30, null=True)),
                ('house', models.CharField(blank=True, max_length=30, null=True)),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('flat', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=75)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('TEMPORARILY_CLOSED', 'Temporarily closed'), ('WORKING', 'Working'), ('CLOSED', 'Closed')], max_length=6)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='locations.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
