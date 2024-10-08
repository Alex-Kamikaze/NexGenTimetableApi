# Generated by Django 5.1.1 on 2024-09-08 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0006_alter_timetable_options_substitution'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100, verbose_name='Название вида справки')),
            ],
        ),
        migrations.CreateModel(
            name='CertificateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_fio', models.CharField(max_length=100, verbose_name='ФИО студента')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('organization_full_name', models.TextField(blank=True, verbose_name='Полное название организации')),
                ('voenkomat_full_name', models.TextField(blank=True, verbose_name='Полное название военкомата')),
                ('completed', models.BooleanField(default=False, verbose_name='Справка выдана')),
                ('student_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='timetable.group', verbose_name='Группа студента')),
                ('certificate_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='document_ordering.certificatetype', verbose_name='Вид справки')),
            ],
            options={
                'verbose_name': 'Заказ выдачи справки',
                'verbose_name_plural': 'Заказы выдачи справок',
            },
        ),
    ]
