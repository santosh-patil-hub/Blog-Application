# Generated by Django 4.2.10 on 2024-09-25 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_application', '0005_alter_comment_blog_alter_like_blog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
