# Generated by Django 4.2.4 on 2023-08-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfiguration',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
