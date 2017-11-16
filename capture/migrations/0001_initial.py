# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 22:51
from __future__ import unicode_literals

import disposable_email_checker.fields
from django.db import migrations, models


def add_email_template(apps, schema_editor):
    apps.get_model('post_office.EmailTemplate').objects.get_or_create(
        name='introduction_email',
        subject='This is an introduction email!',
        content='Hi {{ name }}, here are some details.',
        html_content='Hi <strong>{{ name }}</strong>, here are some details.',
    )


def remove_email_template(apps, schema_editor):
    apps.get_model('post_office.EmailTemplate').objects.filter(
        name='introduction_email',
    ).all().delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post_office', '0005_auto_20170515_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', disposable_email_checker.fields.DisposableEmailField(max_length=254)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('updated_date_time', models.DateTimeField(auto_now=True)),
                ('chase_date', models.DateField(blank=True, null=True, verbose_name='Date to chase up lead.')),
            ],
        ),
        migrations.RunPython(add_email_template, remove_email_template)
    ]
