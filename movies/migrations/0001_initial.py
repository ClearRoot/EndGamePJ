# Generated by Django 2.1.8 on 2019-05-09 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtype', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', models.TextField()),
                ('open_date', models.CharField(max_length=10)),
                ('audience', models.IntegerField()),
                ('image', models.TextField()),
                ('grade', models.CharField(max_length=30)),
                ('nations', models.CharField(max_length=30)),
                ('show_time', models.IntegerField()),
                ('genres', models.ManyToManyField(blank=True, related_name='movies', to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='MovieRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=8)),
                ('rank', models.IntegerField()),
                ('rank_inten', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director', models.CharField(blank=True, max_length=50)),
                ('actor', models.CharField(blank=True, max_length=150)),
                ('movies', models.ManyToManyField(blank=True, related_name='peoples', to='movies.Movie')),
            ],
        ),
    ]
