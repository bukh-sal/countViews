# Generated by Django 3.2.16 on 2022-11-29 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Request Summary',
                'verbose_name_plural': 'Requests Summary',
            },
        ),
        migrations.AddIndex(
            model_name='requestsummary',
            index=models.Index(fields=['date'], name='core_reques_date_8b747e_idx'),
        ),
    ]
