# Generated by Django 2.2.5 on 2019-10-05 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20191005_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='slug',
        ),
    ]