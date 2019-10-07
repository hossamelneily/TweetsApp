# Generated by Django 2.2.5 on 2019-09-29 07:57

import accounts.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=120, unique=True, validators=[django.core.validators.RegexValidator(code='Invalid UserName', message='The username must be Aplanumeric or contain any of the following @ . - +', regex='[0-9a-zA-Z@.-+]*')], verbose_name='User Name')),
                ('firstname', models.CharField(blank=True, max_length=120, null=True, verbose_name='First Name')),
                ('lastname', models.CharField(blank=True, max_length=120, null=True, verbose_name='Last Name')),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.content_file_name, verbose_name='Profile Picture')),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
