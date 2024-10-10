# Generated by Django 4.2.16 on 2024-10-10 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0002_alter_profile_city_alter_profile_email_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusMessage",
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
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("message", models.CharField(max_length=280)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="status_messages",
                        to="mini_fb.profile",
                    ),
                ),
            ],
        ),
    ]
