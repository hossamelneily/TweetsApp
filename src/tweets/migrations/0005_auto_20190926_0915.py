# Generated by Django 2.2.5 on 2019-09-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_tweet_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-timestamp'], 'verbose_name': 'MyTweet', 'verbose_name_plural': 'tweets'},
        ),
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]
