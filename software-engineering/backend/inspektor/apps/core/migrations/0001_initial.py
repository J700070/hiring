# Generated by Django 5.0.1 on 2024-02-06 06:28

import django.db.models.deletion
import inspektor.apps.core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Case",
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
                (
                    "open_datetime",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                ("close_datetime", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "case",
            },
        ),
        migrations.CreateModel(
            name="Image",
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
                ("capture_datetime", models.DateTimeField()),
                (
                    "file",
                    models.ImageField(
                        upload_to=inspektor.apps.core.models.get_image_path
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="core.case",
                    ),
                ),
            ],
            options={
                "db_table": "image",
            },
        ),
    ]