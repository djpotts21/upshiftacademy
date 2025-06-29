# Generated by Django 5.2.3 on 2025-06-26 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_programme_hero_image_programme_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrerequisiteProgrammes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='programme',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='programme',
            name='length',
            field=models.PositiveIntegerField(default=0, help_text='Length in weeks'),
        ),
        migrations.AddField(
            model_name='programme',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, help_text='Other programmes that must be completed before this one', related_name='PrerequisiteProgrammes', to='courses.programme'),
        ),
        migrations.AddField(
            model_name='programme',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
