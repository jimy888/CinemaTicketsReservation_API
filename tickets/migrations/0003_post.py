# Generated by Django 3.2.10 on 2021-12-28 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_remove_movie_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.guest')),
            ],
        ),
    ]