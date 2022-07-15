# pylint: disable=invalid-name

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('page_title', models.CharField(max_length=20)),
            ],
        ),
    ]
