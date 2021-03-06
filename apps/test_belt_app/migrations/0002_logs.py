# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_belt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to='test_belt_app.Users')),
            ],
        ),
    ]
