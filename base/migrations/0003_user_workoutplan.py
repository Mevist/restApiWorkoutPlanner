# Generated by Django 4.0.4 on 2022-05-17 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_exercise_repetitions_alter_exercise_sets'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('password', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(blank=True, choices=[('Power', 'Power'), ('Speed', 'Speed'), ('Flexibility', 'Flexibility')], max_length=100, null=True)),
                ('exercises', models.ManyToManyField(to='base.exercise')),
            ],
        ),
    ]