# Generated by Django 3.1.7 on 2021-03-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('board', models.CharField(choices=[('notice', '공지'), ('free', '자유게시판'), ('anon', '익명게시판')], default='free', max_length=10)),
                ('view_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
