# Generated by Django 4.2.5 on 2023-09-27 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('tags', models.TextField()),
                ('file', models.FileField(upload_to='uploads/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]