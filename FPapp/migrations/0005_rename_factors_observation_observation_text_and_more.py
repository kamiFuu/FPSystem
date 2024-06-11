# Generated by Django 5.0.6 on 2024-05-31 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FPapp', '0004_rename_lessonstructure_lecturestructure'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observation',
            old_name='factors',
            new_name='observation_text',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='focus_loss_time',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='researcher',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='student',
        ),
        migrations.AddField(
            model_name='observation',
            name='end_time',
            field=models.TimeField(default='23:59:59'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='start_time',
            field=models.TimeField(default='23:59:59'),
            preserve_default=False,
        ),
    ]
