# Generated by Django 4.1 on 2023-05-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrank',
            name='top_score',
            field=models.IntegerField(default=0),
        ),
    ]
