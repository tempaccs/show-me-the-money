# Generated by Django 3.0.3 on 2020-02-24 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reference", models.CharField(max_length=10, unique=True)),
                ("account", models.CharField(max_length=10)),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "type",
                    models.CharField(
                        choices=[("outflow", "outflow"), ("inflow", "inflow")],
                        max_length=20,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("groceries", "groceries"),
                            ('"salary",', '"salary",'),
                            ("transfer", "transfer"),
                            ("rent", "rent"),
                            ("savings", "savings"),
                            ("other", "other"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="customers.Customer",
                    ),
                ),
            ],
        ),
    ]
