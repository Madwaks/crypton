# Generated by Django 3.2 on 2021-05-02 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("decision_maker", "0002_auto_20210502_1716")]

    operations = [
        migrations.AddField(
            model_name="symbolindicator",
            name="time_unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1m", "Minutes1"),
                    ("5m", "Minutes5"),
                    ("15m", "Minutes15"),
                    ("30m", "Minutes30"),
                    ("1h", "Hour1"),
                    ("4h", "Hour4"),
                    ("1d", "Day1"),
                    ("1w", "Week1"),
                    ("1M", "Month1"),
                ],
                max_length=128,
                null=True,
            ),
        )
    ]