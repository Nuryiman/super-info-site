# Generated by Django 5.0.7 on 2024-08-04 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_publicationcomment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationcomment',
            name='publication',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.publication'),
        ),
    ]
