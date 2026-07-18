from django.db import migrations


PLANS = [
    ("Ribural Level 1", 10000, 1500, 20),
    ("Ribural Level 2", 20000, 3000, 20),
    ("Ribural Level 3", 30000, 4500, 20),
    ("Ribural Level 4", 50000, 7500, 20),
    ("Ribural Level 5", 80000, 12000, 20),
    ("Ribural Level 6", 90000, 13500, 20),
    ("Ribural Level 7", 150000, 22000, 20),
    ("Ribural Level 8", 200000, 28000, 20),
    ("Ribural Level 9", 300000, 33000, 20),
    ("Ribural Level 10", 400000, 44000, 20),
    ("Ribural Level 11", 500000, 55000, 20),
    ("Ribural Level 12", 700000, 77000, 20),
    ("Ribural Level 13", 800000, 88000, 20),
    ("Ribural Level 14", 900000, 99000, 20),
]


def seed_plans(apps, schema_editor):
    InvestmentPlan = apps.get_model("investments", "InvestmentPlan")
    for index, (name, amount, daily_income, duration_days) in enumerate(PLANS, start=1):
        InvestmentPlan.objects.update_or_create(
            name=name,
            defaults={
                "amount": amount,
                "daily_income": daily_income,
                "duration_days": duration_days,
                "sort_order": index,
                "is_active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("investments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_plans, migrations.RunPython.noop),
    ]
