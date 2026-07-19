from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('ussername', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
                ('mobile_no', models.BigIntegerField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]
