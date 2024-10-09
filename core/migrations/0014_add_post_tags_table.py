from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_merge_20240917_1712'),  # Make sure this matches your last migration
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.post')),
                ('tag', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.tag')),
            ],
            options={
                'db_table': 'core_post_tags',
            },
        ),
    ]