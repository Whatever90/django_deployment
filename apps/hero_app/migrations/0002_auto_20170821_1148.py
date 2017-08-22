# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hero_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='powers',
            name='hero',
        ),
        migrations.AddField(
            model_name='heroes',
            name='power',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pow', to='hero_app.powers'),
            preserve_default=False,
        ),
    ]
