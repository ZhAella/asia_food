# Generated by Django 5.0.2 on 2024-04-01 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.DateTimeField(auto_created=True, auto_now=True, null=True),
        ),
    ]
