# Generated by Django 3.2 on 2021-04-25 17:41

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "timestamp",
                    models.CharField(max_length=512, primary_key=True, serialize=False),
                ),
                ("open", models.FloatField(max_length=128, verbose_name="open_price")),
                (
                    "close",
                    models.FloatField(max_length=128, verbose_name="close_price"),
                ),
                ("high", models.FloatField(max_length=128, verbose_name="high_price")),
                ("low", models.FloatField(max_length=128, verbose_name="low_price")),
                ("volume", models.FloatField(verbose_name="volumes")),
                ("close_time", models.CharField(blank=True, max_length=512, null=True)),
                ("time_unit", models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Symbol",
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
                ("name", models.CharField(max_length=20)),
                ("base_asset", models.CharField(max_length=10)),
                ("quote_asset", models.CharField(max_length=10)),
                (
                    "order_types",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64, null=True), size=10
                    ),
                ),
            ],
            options={
                "verbose_name": "CryptoPair",
                "verbose_name_plural": "CryptoPairs",
                "ordering": ("name", "base_asset", "quote_asset"),
            },
        ),
        migrations.AddConstraint(
            model_name="symbol",
            constraint=models.UniqueConstraint(
                fields=("name", "base_asset", "quote_asset"),
                name="unique_per_symbol_pairs",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="symbol",
            field=models.ForeignKey(
                max_length=128,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="quotes",
                to="crypto.symbol",
            ),
        ),
    ]
