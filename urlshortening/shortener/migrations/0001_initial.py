# Generated by Django 4.2.9 on 2024-05-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="URL",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("original_url", models.URLField()),
                ("shortened_url", models.CharField(max_length=20, unique=True)),
                ("user_email", models.CharField(max_length=200)),
                ("view_count", models.BigIntegerField(default=0)),
            ],
        ),
    ]
