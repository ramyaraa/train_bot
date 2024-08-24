# Generated by Django 5.1 on 2024-08-23 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='time',
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('python', 'Python'), ('java', 'Java'), ('javascript', 'JavaScript'), ('webdev', 'Web Development'), ('machinelearning', 'Machine Learning'), ('other', 'Other')], default='other', max_length=50),
        ),
    ]
