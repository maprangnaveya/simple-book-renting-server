# Generated by Django 5.0.1 on 2024-02-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentallog',
            name='status',
            field=models.CharField(choices=[('ON_GOING', 'On Going'), ('RETURNED', 'Returned'), ('OVERDUE', 'Overdue')], default='ON_GOING', max_length=8, verbose_name='Reant Status'),
        ),
    ]