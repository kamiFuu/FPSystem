# Generated by Django 5.0.6 on 2024-06-03 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPapp', '0005_rename_factors_observation_observation_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturestructure',
            name='material',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]