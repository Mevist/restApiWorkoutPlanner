# Generated by Django 4.0.4 on 2022-05-17 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('sets', models.DecimalField(blank=True, decimal_places=0, max_digits=2)),
                ('repetitions', models.DecimalField(blank=True, decimal_places=0, max_digits=2)),
            ],
        ),
    ]
