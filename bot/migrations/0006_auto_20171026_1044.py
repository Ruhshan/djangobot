# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20171026_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.CharField(max_length=127, verbose_name='Item Image'),
        ),
    ]
