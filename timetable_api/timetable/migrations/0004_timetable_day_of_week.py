# Generated by Django 5.1.1 on 2024-09-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_alter_subject_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='day_of_week',
            field=models.CharField(choices=[('0', 'Понедельник'), ('1', 'Вторник'), ('2', 'Среда'), ('3', 'Четверг'), ('4', 'Пятница')], default='0', max_length=1, verbose_name='День недели'),
        ),
    ]
