# Generated manually to make video file optional for URL-only entries.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrections', '0002_remove_correction_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
