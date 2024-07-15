# Generated by Django 4.2.14 on 2024-07-14 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Singer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singer_id', models.CharField(max_length=50, unique=True)),
                ('singer_name', models.CharField(max_length=100)),
                ('image_url', models.URLField()),
                ('bio', models.TextField()),
                ('original_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.CharField(max_length=50, unique=True)),
                ('song_name', models.CharField(max_length=100)),
                ('image_url', models.URLField()),
                ('lyrics', models.TextField()),
                ('original_url', models.URLField()),
                ('singer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='music.singer')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='music.song')),
            ],
        ),
    ]
