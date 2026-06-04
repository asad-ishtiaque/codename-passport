from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_groups_and_tokens'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DROP TABLE IF EXISTS auth_group_permissions CASCADE;
                DROP TABLE IF EXISTS auth_group CASCADE;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
