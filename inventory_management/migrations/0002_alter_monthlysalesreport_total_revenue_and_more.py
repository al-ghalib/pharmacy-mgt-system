# Generated by Django 5.1.5 on 2025-02-07 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalesreport',
            name='total_revenue',
            field=models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=12),
        ),
        migrations.AlterField(
            model_name='monthlysalesreport',
            name='total_sales',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='new_stock',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='previous_stock',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
