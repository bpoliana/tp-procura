# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-14 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='n_user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='n_user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='n_user',
            name='password',
        ),
        migrations.AddField(
            model_name='n_user',
            name='utype',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
